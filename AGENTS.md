# AGENTS.md

Rules for any AI agent working on this site (coding-finance.github.io), the personal website of Emanuelle Sedita.

## Source of truth

- `cv.pdf` is the source for all career content. Do not invent, round, or embellish numbers, titles, dates, or employers.
- Exception: Emanuelle supplied extra Johnson & Johnson content from an older resume (three more Manager bullets, the 2018–2020 program split into two roles, and the Jabil bullet). That content is approved and lives only in `index.html`.
- Exception: the header tagline (two lines: "MBA Candidate at Columbia Business School" / "Incoming Investment Banking Associate at Citi") was written by Emanuelle and is approved, even though "Incoming Associate" is not on the CV. Do not add any other offer details.
- Roles show title and dates only (no one-line summaries). Emanuelle removed them to cut text.
- Acronyms are approved on the site (e.g., IB, HC, GTM, ICs, SC, S&M, SMIF, ALPFA, FLDP, Sr., vs.) in place of the CV's spelled-out words. Use `<abbr title="...">` for less common ones. "FLDP" appears only in the role titles (full name on hover), with no separate label.
- Exception (Emanuelle's edits to CBS): Memberships read "HCIA, Football Club, Ski Club, Gourmet Club, Poker Club, The Consortium" (CV says Healthcare Industry Association and Snow Sports Club). The GMAT score is intentionally not shown. Abbreviating is the only allowed change to bullet wording.
- If the site and the CV disagree, flag it to Emanuelle. Do not silently "fix" either one.
- Exception: on the site, Seton Hall has a "Memberships" line holding Student Managed Investment Fund and Association of Latino Professionals For America; "Leadership" lists only Hall Street Fund Vice President. Approved by Emanuelle.
- Site sections, in order: Education, Experience. The CV's Additional Information section is intentionally left off the site (Emanuelle's choice).

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

## Style

- Professional and restrained. This is a finance and investment banking profile, not a portfolio of effects.
- Colors: blue, white, black only (plus grays derived from them). Primary blue `#0B3D91`, accent blue `#1E6FD9`, black `#0A0A0A`, white `#FFFFFF`.
- Typography: one clean sans-serif family; clear hierarchy; no decorative fonts.
- Navigation: no separate navigation bar. The page is a single screen; contact links (LinkedIn, GitHub, Email) sit in the blue header.
- Plain static HTML and CSS. No frameworks or build steps unless Emanuelle asks.
- Must work on phones (no horizontal scroll) and be accessible: semantic HTML, alt text, visible focus states, sufficient contrast.
- Writing: plain language, no buzzwords, no exaggeration. Keep CV wording as written, except approved acronyms. Keep text light; Emanuelle prefers less text on screen.
