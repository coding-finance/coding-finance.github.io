"""Fetch Emanuelle's Sleeper fantasy football data and write data/fantasy.json.

Run by .github/workflows/fantasy.yml on a schedule. Uses only Sleeper's public,
read-only API (https://docs.sleeper.com) and the Python standard library.

Privacy: the output never contains Sleeper usernames, user IDs, team names, or
league names. Other managers appear only as generic "Team <n>".
"""

import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

API = "https://api.sleeper.app/v1"
# Kept out of the public repo: set as GitHub Actions secrets (or env vars when run locally).
# Anyone with a Sleeper league ID can read that league, so never hard-code or print these.
MY_USER_ID = os.environ.get("SLEEPER_USER_ID", "").strip()
LEAGUE_IDS = [x.strip() for x in os.environ.get("SLEEPER_LEAGUE_IDS", "").split(",") if x.strip()]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "data", "fantasy.json")
# Sleeper asks that the large players file be fetched at most once a day.
PLAYERS_CACHE = os.environ.get("PLAYERS_CACHE", os.path.join(ROOT, ".cache", "players.json"))

SLOT_LABELS = {"FLEX": "FLEX", "WRRB_FLEX": "W/R", "REC_FLEX": "W/T", "SUPER_FLEX": "SF", "DEF": "DEF"}


def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "personal-site-fantasy-updater"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 2:
                # Generic message on purpose: the URL can contain a private league ID and logs are public.
                raise SystemExit(f"Sleeper request failed ({type(e).__name__})") from None
            time.sleep(3)


def load_players():
    fresh = os.path.exists(PLAYERS_CACHE) and time.time() - os.path.getmtime(PLAYERS_CACHE) < 24 * 3600
    if not fresh:
        os.makedirs(os.path.dirname(PLAYERS_CACHE), exist_ok=True)
        players = get("/players/nfl")
        slim = {
            pid: {"n": p.get("full_name") or f"{p.get('first_name', '')} {p.get('last_name', '')}".strip(),
                  "p": p.get("position"), "t": p.get("team")}
            for pid, p in players.items()
        }
        with open(PLAYERS_CACHE, "w", encoding="utf-8") as f:
            json.dump(slim, f)
    with open(PLAYERS_CACHE, encoding="utf-8") as f:
        return json.load(f)


_PROJ = {}


def projections(season, week):
    """Sleeper's weekly player projections (unofficial but public endpoint). Cached per run."""
    key = (season, week)
    if key not in _PROJ:
        req = urllib.request.Request(
            f"https://api.sleeper.app/projections/nfl/{season}/{week}?season_type=regular"
            + "".join(f"&position[]={pos}" for pos in ("QB", "RB", "WR", "TE", "K", "DEF")),
            headers={"User-Agent": "personal-site-fantasy-updater"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                _PROJ[key] = {row["player_id"]: row.get("stats") or {} for row in json.load(r)}
        except Exception:
            _PROJ[key] = {}
    return _PROJ[key]


def projected_total(starters, proj, scoring, players):
    """Project a lineup with the league's own scoring rules.
    Kickers and defenses use Sleeper's pre-computed points (their stat buckets don't match league settings)."""
    total = 0.0
    for pid in starters or []:
        stats = proj.get(pid) or {}
        if (players.get(pid) or {}).get("p") in ("K", "DEF") or not pid.isdigit():
            total += stats.get("pts_ppr", 0)
        else:
            total += sum(v * scoring.get(k, 0) for k, v in stats.items() if isinstance(v, (int, float)))
    return round(total, 1)


def player_info(players, pid):
    p = players.get(pid) or {}
    name = p.get("n") or pid
    if p.get("p") == "DEF":
        name = f"{pid} D/ST"
    return {"id": pid, "name": name, "pos": p.get("p") or "", "team": p.get("t") or ""}


def short_name(full):
    parts = full.split()
    if len(parts) >= 2 and not full.endswith("D/ST"):
        return f"{parts[0][0]}. {' '.join(parts[1:])}"
    return full


def build_league(league_id, label, state, players):
    league = get(f"/league/{league_id}")
    rosters = get(f"/league/{league_id}/rosters")
    settings = league.get("settings", {})
    season_week = int(state.get("week") or 1)
    start_week = int(settings.get("start_week") or 1)
    playoff_start = int(settings.get("playoff_week_start") or 15)
    playoff_teams = int(settings.get("playoff_teams") or 6)
    last_reg_week = playoff_start - 1
    current_week = max(start_week, min(season_week, last_reg_week))

    names, my_rid = {}, None
    for r in rosters:
        rid = r["roster_id"]
        names[rid] = f"Team {rid}"
        if r.get("owner_id") == MY_USER_ID or MY_USER_ID in (r.get("co_owners") or []):
            my_rid = rid
    if my_rid is None:
        raise SystemExit(f"Could not find my roster in {label}")

    def pts(s, key):
        return round(s.get(key, 0) + s.get(key + "_decimal", 0) / 100, 2)

    table = []
    for r in rosters:
        s = r.get("settings", {})
        table.append({"rid": r["roster_id"], "name": names[r["roster_id"]], "w": s.get("wins", 0),
                      "l": s.get("losses", 0), "t": s.get("ties", 0), "pf": pts(s, "fpts"), "pa": pts(s, "fpts_against"),
                      "me": r["roster_id"] == my_rid})
    table.sort(key=lambda x: (-(x["w"] + x["t"] / 2), -x["pf"]))
    for i, row in enumerate(table, 1):
        row["rank"] = i
    by_pf = sorted(table, key=lambda x: -x["pf"])
    me = next(x for x in table if x["me"])
    pf_rank = next(i for i, x in enumerate(by_pf, 1) if x["me"])
    cutoff_gap = None
    if len(table) > playoff_teams:
        first_out = table[playoff_teams]
        last_in = table[playoff_teams - 1]
        if me["rank"] <= playoff_teams:
            cutoff_gap = (me["w"] + me["t"] / 2) - (first_out["w"] + first_out["t"] / 2)
        else:
            cutoff_gap = (me["w"] + me["t"] / 2) - (last_in["w"] + last_in["t"] / 2)

    my_roster = next(r for r in rosters if r["roster_id"] == my_rid)
    streak = (my_roster.get("metadata") or {}).get("streak")

    schedule, weeks = [], {}
    for wk in range(start_week, last_reg_week + 1):
        data = get(f"/league/{league_id}/matchups/{wk}")
        weeks[wk] = data
        mine = next((m for m in data if m["roster_id"] == my_rid), None)
        if not mine:
            continue
        opp = next((m for m in data if m.get("matchup_id") is not None and m.get("matchup_id") == mine.get("matchup_id")
                    and m["roster_id"] != my_rid), None)
        my_pts, opp_pts = round(mine.get("points") or 0, 2), round((opp or {}).get("points") or 0, 2)
        if wk < season_week:
            status = "final"
            result = "W" if my_pts > opp_pts else "L" if my_pts < opp_pts else "T"
        elif wk == season_week:
            status = "live" if (my_pts or opp_pts) else "upcoming"
            result = None
        else:
            status, result = "upcoming", None
        game = {"week": wk, "my": my_pts, "their": opp_pts, "status": status, "result": result}
        if wk == current_week and status == "upcoming" and opp:
            # Before kickoff: show the matchup with projected scores
            proj = projections(state.get("season"), wk)
            scoring = league.get("scoring_settings") or {}
            game.update(opp=names.get(opp["roster_id"]),
                        proj_my=projected_total(mine.get("starters"), proj, scoring, players),
                        proj_their=projected_total(opp.get("starters"), proj, scoring, players))
        schedule.append(game)

    this_week = next((g for g in schedule if g["week"] == current_week), None)

    # Lineup for the current week
    cur = next((m for m in weeks.get(current_week, []) if m["roster_id"] == my_rid), {}) or {}
    slots = [s for s in league.get("roster_positions", []) if s not in ("BN", "IR", "TAXI")]
    starters_ids = cur.get("starters") or my_roster.get("starters") or []
    pp = cur.get("players_points") or {}
    starters = []
    for slot, pid in zip(slots, starters_ids):
        if pid in (None, "0"):
            starters.append({"slot": SLOT_LABELS.get(slot, slot), "id": None, "name": "Empty", "pos": "", "team": "", "pts": 0})
            continue
        info = player_info(players, pid)
        starters.append({"slot": SLOT_LABELS.get(slot, slot), **info, "pts": round(pp.get(pid, 0), 2)})
    starter_set = set(starters_ids)
    bench = []
    for pid in (my_roster.get("players") or []):
        if pid in starter_set:
            continue
        info = player_info(players, pid)
        bench.append({"slot": "BN", **info, "pts": round(pp.get(pid, 0), 2)})
    bench.sort(key=lambda x: -x["pts"])

    # Key player: top-scoring starter this week, or last week's if this week hasn't started
    key = None
    live_starters = [s for s in starters if s["name"] != "Empty"]
    if live_starters and max(s["pts"] for s in live_starters) > 0:
        top = max(live_starters, key=lambda s: s["pts"])
        key = {"label": f"Top scorer, week {current_week}", **top}
    elif current_week - 1 >= start_week:
        prev = next((m for m in weeks.get(current_week - 1, []) if m["roster_id"] == my_rid), None)
        if prev and prev.get("starters_points"):
            idx = max(range(len(prev["starters"])), key=lambda i: prev["starters_points"][i])
            key = {"label": f"Top scorer, week {current_week - 1}",
                   **player_info(players, prev["starters"][idx]), "pts": round(prev["starters_points"][idx], 2)}
    if key:
        key["short"] = short_name(key["name"])

    return {
        "label": label,
        "rank": me["rank"], "teams": len(table),
        "record": {"w": me["w"], "l": me["l"], "t": me["t"]},
        "pf": me["pf"], "pf_rank": pf_rank, "streak": streak,
        "playoff_teams": playoff_teams, "cutoff_gap": cutoff_gap,
        "week": current_week, "this_week": this_week, "key_player": key,
        "schedule": schedule,
        "lineup": {"starters": starters, "bench": bench},
    }


def main():
    if not MY_USER_ID or not LEAGUE_IDS:
        raise SystemExit("Set SLEEPER_USER_ID and SLEEPER_LEAGUE_IDS (comma-separated) first.")
    state = get("/state/nfl")
    players = load_players()
    out = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "season": state.get("season"),
        "week": state.get("week"),
        "leagues": [build_league(lid, f"League {i}", state, players) for i, lid in enumerate(LEAGUE_IDS, 1)],
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    old = None
    if os.path.exists(OUT_PATH):
        with open(OUT_PATH, encoding="utf-8") as f:
            old = json.load(f)
    if old and {k: v for k, v in old.items() if k != "updated"} == {k: v for k, v in out.items() if k != "updated"}:
        print("No changes")
        return
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    sys.exit(main())
