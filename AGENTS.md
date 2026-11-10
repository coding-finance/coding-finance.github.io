# AGENTS.md

Rules for any AI agent working on this site (coding-finance.github.io), the personal website of Emanuelle Sedita.

## Source of truth

- `cv.pdf` is the source for all career content. Do not invent, round, or embellish numbers, titles, dates, or employers.
- Exception: Emanuelle supplied extra Johnson & Johnson content from an older resume (three more Manager bullets, the 2018–2020 program split into two roles, and the Jabil bullet). That content is approved and lives only in `index.html`.
- Exception: the header tagline (two lines: "MBA Candidate at Columbia Business School" / "Incoming Investment Banking Associate at Citi") was written by Emanuelle and is approved, even though "Incoming Associate" is not on the CV. Do not add any other offer details.
- Roles show title and dates only (no one-line summaries). Emanuelle removed them to cut text.
- Acronyms are approved on the site (e.g., IB, HC, GTM, ICs, SC, S&M, SMIF, ALPFA, FLDP, SFA, FA, AFA, Sr., vs.) in place of the CV's spelled-out words. Use `<abbr title="...">` for less common ones. "FLDP" appears only in the role titles (full name on hover), with no separate label.
- Exception: no "Memberships" lines anywhere on the site (Emanuelle removed them for CBS and Seton Hall). The GMAT score is intentionally not shown. Abbreviating is the only allowed change to bullet wording.
- If the site and the CV disagree, flag it to Emanuelle. Do not silently "fix" either one.
- Exception: CBS "Leadership" reads "Investment Banking Club VP of Finance" (CV says AVP; Emanuelle changed it to VP).
- Exception: Seton Hall "Leadership" lists only Hall Street Fund Vice President (SMIF and ALPFA are intentionally left off). Approved by Emanuelle.
- Site sections, in order: Education, Experience, then Fantasy Football (personal section requested by Emanuelle). The CV's Additional Information section is intentionally left off the site (Emanuelle's choice).

## Never publish

- Phone number, home address, date of birth, or any government ID.
- Personal (non-school, non-work) email addresses unless Emanuelle provides one for the site.
- Salary, compensation, or offer details.
- Non-public deal information: client names, deal sizes, or deal terms that are not already on the CV. Never add detail beyond what the CV says.
- Confidential employer material (Citi, Johnson & Johnson): internal documents, decks, models, screenshots. (Public company and school logos in `images/logos/` are approved by Emanuelle for identifying employers and schools.)
- Secrets of any kind: API keys, tokens, passwords, `.env` files.
- Photos of other people, or names of colleagues, classmates, or references.

## Ask Emanuelle first

- Before any `git commit`, `git push`, or change to GitHub settings, repos, or GitHub Pages.
- Before publishing or committing `cv.pdf` itself (it contains the phone number).
- Before adding any contact detail, photo, or social profile not already approved. Approved so far: Columbia email, LinkedIn (https://www.linkedin.com/in/emanuelle-sedita/), GitHub (https://github.com/coding-finance), headshot (`images/headshot.jpeg`).
- Before deleting or overwriting existing files.
- Before adding third-party scripts, analytics, trackers, cookies, or forms. Approved so far: GoatCounter (`https://gc.zgo.at/count.js`, dashboard at https://emanuellesedita.goatcounter.com). No cookies; no other analytics.
- Before rewording CV bullets beyond formatting (e.g., shortening or changing claims).
- Before adding new pages or sections not requested.

## Hosting

- Live at https://emanuellesedita.com (GitHub Pages, repo `coding-finance/coding-finance.github.io`, branch `main`, HTTPS enforced). `www` and `coding-finance.github.io` redirect there.
- The `CNAME` file holds the custom domain. Never delete or edit it, or the domain link breaks.
- DNS is managed by Emanuelle in Squarespace (4 A records to GitHub Pages IPs, `www` CNAME to `coding-finance.github.io`, plus a `_github-pages-challenge-coding-finance` TXT record for domain verification). Do not tell Emanuelle to remove these.

## Fantasy Football section

- Shows Emanuelle's two Sleeper teams as "League 1" and "League 2": one slim row each (side by side on wide screens), labeled "League 1" / "League 2" with total points, then position out of 12, record with season form underneath (e.g. WWLWWWLWW, wins in teal), this week's score (the side that's ahead is in teal; no "live"/"leading" labels; no opponent name once games start), or before kickoff the projected score "Projected vs Team n" (each starter's Sleeper projection, scored with the league's own settings; Sleeper's points for K and DEF), and "Player of the Week" (full name with position, photo, points next to the name with the week underneath). Clicking a row expands Lineup / Schedule (week chips). No standings table or other teams' records (Emanuelle's choice). Approved by Emanuelle.
- Look: deliberately different from the résumé, Sleeper-style. Dark panel (`#10161F`), teal accent (`#1FD1C1`) for wins / when Emanuelle is ahead, red (`#FF5C6C`) for losses / when Emanuelle is behind (live or projected; the opponent's score stays gray), and Barlow Condensed (self-hosted in `fonts/`, license `fonts/OFL-barlow.txt`). These colors and this font are allowed only inside the Fantasy Football section; the rest of the site keeps the Style rules below. Keep it compact.
- Data: `.github/workflows/fantasy.yml` runs `scripts/update_fantasy.py` (Python standard library only) on a schedule, which reads Sleeper's public read-only API and commits `data/fantasy.json`. `js/fantasy.js` renders it. This is the one approved use of JavaScript and of a scheduled build job.
- Privacy: never put Sleeper usernames, user IDs, or league names in `data/fantasy.json` or on the page. Other managers appear only as generic "Team <n>" (never their custom team names). Cards are titled "League 1" / "League 2", never the league or team name.
- Sleeper has no API keys: anyone with a league ID can read that league. So Emanuelle's Sleeper user ID and league IDs live only in GitHub Actions secrets (`SLEEPER_USER_ID`, `SLEEPER_LEAGUE_IDS`). Never hard-code them, commit them, print them in logs, or put them in `data/fantasy.json`.
- Always escape data before inserting it into the page (see `esc()` in `js/fantasy.js`).
- Player photos (and defense team logos) load directly from Sleeper's image CDN (`sleepercdn.com`), approved by Emanuelle. No other third-party images.
- Labels are spelled out ("Week", "points"), not "Wk"/"pts". No "updated"/source/week text in the section header.
- Projections come from Sleeper's public but undocumented `/projections` endpoint; if it fails, the card just shows 0.0–0.0 for the upcoming week.
- Respect Sleeper's guidance: fetch the large `/players/nfl` file at most once a day (cached in `.cache/`, not committed).

## Style

- Professional and restrained. This is a finance and investment banking profile, not a portfolio of effects.
- Exception: the ✈️ favicon is the only decorative touch approved by Emanuelle. The "Send Message" button is plain text (a drawn plane and button emojis were tried and rejected).
- Colors: blue, white, black only (plus grays derived from them). Primary blue `#0B3D91`, accent blue `#1E6FD9`, black `#0A0A0A`, white `#FFFFFF`.
- Typography: one clean sans-serif family; clear hierarchy; no decorative fonts. Inter is self-hosted from `fonts/` (license in `fonts/OFL.txt`); do not load fonts from Google or other CDNs.
- Link previews: Open Graph tags in `<head>` use the headshot and the tagline. Keep `og:description` and the meta description in sync with the header tagline.
- Navigation: no separate navigation bar. The page is a single screen; the blue header has two buttons, "Send Message" (mailto Columbia email) then "LinkedIn". No GitHub link on the site (Emanuelle's choice).
- Plain static HTML and CSS. No frameworks or build steps unless Emanuelle asks (exception: the Fantasy Football data job and `js/fantasy.js`).
- Must work on phones (no horizontal scroll) and be accessible: semantic HTML, alt text, visible focus states, sufficient contrast.
- Writing: plain language, no buzzwords, no exaggeration. Keep CV wording as written, except approved acronyms. Keep text light; Emanuelle prefers less text on screen.
