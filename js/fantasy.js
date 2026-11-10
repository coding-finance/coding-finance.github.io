// Renders the Fantasy Football section from data/fantasy.json
// (refreshed by .github/workflows/fantasy.yml). No third-party code.
(function () {
  var root = document.getElementById("ff-leagues");
  if (!root) return;

  // Always escape data before inserting it into the page.
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function suffix(n) {
    var s = ["th", "st", "nd", "rd"], v = n % 100;
    return s[(v - 20) % 10] || s[v] || s[0];
  }
  function pts(n) { return (Math.round(n * 10) / 10).toFixed(1); }
  function rec(r) { return r.w + "–" + r.l + (r.t ? "–" + r.t : ""); }

  // Player headshots (team logo for defenses) served by Sleeper's image CDN.
  function photo(p) {
    if (!p || !p.id) return '<span class="ff-ph-empty" aria-hidden="true"></span>';
    var src = p.pos === "DEF"
      ? "https://sleepercdn.com/images/team_logos/nfl/" + encodeURIComponent(String(p.team || p.id).toLowerCase()) + ".png"
      : "https://sleepercdn.com/content/nfl/players/thumb/" + encodeURIComponent(p.id) + ".jpg";
    return '<img src="' + src + '" alt="" loading="lazy" decoding="async" onerror="this.style.visibility=\'hidden\'">';
  }

  // This week's matchup: my score turns teal when I'm ahead, no "leading/live" text needed.
  function score(g) {
    if (!g) return '<div class="ff-score"></div>';
    if (g.status === "upcoming" && g.proj_my != null) {
      // Before kickoff: next matchup with projected scores
      return '<div class="ff-score proj"><span class="n' + (g.proj_my > g.proj_their ? " up" : g.proj_my < g.proj_their ? " down" : "") + '">' + pts(g.proj_my) + '</span><span class="dash">–</span>' +
        '<span class="n">' + pts(g.proj_their) + "</span>" +
        '<span class="ff-small">Projected vs ' + esc(g.opp).replace(" ", "&nbsp;") + "</span></div>";
    }
    return '<div class="ff-score"><span class="n' + (g.my > g.their ? " up" : g.my < g.their ? " down" : "") + '">' + pts(g.my) + '</span><span class="dash">–</span>' +
      '<span class="n">' + pts(g.their) + "</span>" +
      '<span class="ff-small">Week ' + g.week + (g.status === "final" ? " · Final" : "") + "</span></div>";
  }

  function keyPlayer(L) {
    var kp = L.key_player;
    if (!kp) return '<div class="ff-key"></div>';
    var wk = (kp.label.match(/\d+$/) || [])[0] || L.week;
    return '<div class="ff-key">' + photo(kp) + '<div class="ff-key-txt"><span class="ff-key-name">' + esc(kp.name) + (kp.pos ? " <small>" + esc(kp.pos) + "</small>" : "") + "</span>" +
      '<span class="ff-small">Player of the Week</span></div>' +
      '<div class="ff-key-pts"><span>' + pts(kp.pts) + "<small>points</small></span>" +
      '<span class="ff-small">Week ' + esc(wk) + "</span></div></div>";
  }

  function lineup(L) {
    var item = function (p, bench) {
      return '<div class="ff-pl' + (bench ? " bn" : "") + '"><span class="slot">' + esc(p.slot) + "</span>" + photo(p) +
        '<span class="nm">' + esc(p.name) + (p.team ? "<small>" + esc(p.team) + "</small>" : "") + "</span>" +
        '<span class="pt">' + pts(p.pts) + "</span></div>";
    };
    return '<div class="ff-lineup">' + L.lineup.starters.map(function (p) { return item(p, false); }).join("") +
      (L.lineup.bench.length ? '<p class="ff-sub">Bench</p>' + L.lineup.bench.map(function (p) { return item(p, true); }).join("") : "") +
      "</div>";
  }

  function schedule(L) {
    return '<div class="ff-weeks">' + L.schedule.map(function (g) {
      var cls = "ff-wk" + (g.result === "W" ? " w" : g.result === "L" ? " l" : "") + (g.week === L.week ? " now" : "");
      var r = g.status === "final" ? g.result : g.week === L.week ? "Now" : "–";
      var s = g.status === "upcoming" ? "&nbsp;" : pts(g.my) + "–" + pts(g.their);
      return '<div class="' + cls + '"><span class="ff-small">Week ' + g.week + '</span><span class="r">' + r + '</span><span class="s">' + s + "</span></div>";
    }).join("") + "</div>";
  }

  function row(L, i) {
    var id = "ff" + i;
    // Season form, oldest to newest, e.g. LWWWWLWWW
    var form = L.schedule.filter(function (g) { return g.status === "final" && g.result; }).map(function (g) { return g.result; });
    return '<details class="ff-row"><summary aria-label="' + esc(L.label) + ": " + L.rank + suffix(L.rank) + " of " + L.teams + ", record " + rec(L.record) + '. Show lineup and schedule">' +
      '<div class="ff-sum">' +
        '<span class="ff-nm">' + esc(L.label) + " <span>· " + Math.round(L.pf).toLocaleString("en-US") + " points</span></span>" +
        '<div class="ff-rk"><b>' + L.rank + "<sup>" + suffix(L.rank) + '</sup></b><span class="ff-small">of ' + L.teams + "</span></div>" +
        '<div class="ff-rec"><b>' + rec(L.record) + "</b>" +
          (form.length ? '<span class="ff-form" aria-label="Results by week: ' + form.join(" ") + '">' +
            form.map(function (r) { return '<i class="' + (r === "W" ? "w" : r === "L" ? "l" : "") + '">' + esc(r) + "</i>"; }).join("") + "</span>" : "") +
        "</div>" +
        score(L.this_week) +
        keyPlayer(L) +
        '<span class="ff-chev" aria-hidden="true"></span>' +
      "</div></summary>" +
      '<div class="ff-body"><div class="ff-tabs" role="tablist">' +
        ["Lineup", "Schedule"].map(function (t, j) {
          return '<button type="button" role="tab" id="' + id + "-t" + j + '" aria-controls="' + id + "-p" + j + '" aria-selected="' + (j === 0) + '"' + (j ? ' tabindex="-1"' : "") + ">" + t + "</button>";
        }).join("") +
      "</div>" +
      '<div role="tabpanel" id="' + id + '-p0" aria-labelledby="' + id + '-t0">' + lineup(L) + "</div>" +
      '<div role="tabpanel" id="' + id + '-p1" aria-labelledby="' + id + '-t1" hidden>' + schedule(L) + "</div>" +
      "</div></details>";
  }

  function wireTabs() {
    root.querySelectorAll('[role="tablist"]').forEach(function (list) {
      var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
      function select(tab) {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute("aria-selected", on);
          t.tabIndex = on ? 0 : -1;
          document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
        });
      }
      tabs.forEach(function (tab, i) {
        tab.addEventListener("click", function () { select(tab); });
        tab.addEventListener("keydown", function (e) {
          var n = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
          if (!n) return;
          var next = tabs[(i + n + tabs.length) % tabs.length];
          select(next); next.focus();
        });
      });
    });
  }

  fetch("data/fantasy.json", { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (d) {
      root.innerHTML = d.leagues.map(row).join("");
      wireTabs();
    })
    .catch(function () {
      root.innerHTML = '<p class="ff-note">Fantasy stats are unavailable right now.</p>';
    });
})();
