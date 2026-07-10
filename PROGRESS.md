# ✦ EAUCO Planner Business — Progress Tracker

> **Last updated:** July 10, 2026  
> Update this file every session. GitHub renders checkboxes — click them directly on GitHub to mark things done.

---

## ✅ Phase 0.5 — Maddie's Planner: Real Ephemeris + New Sections
> **Completed:** July 10, 2026

- [x] Real Swiss Ephemeris data pipeline (`tools/generate_ephemeris.py`, `pyswisseph`, Lahiri sidereal, whole-sign houses) — generates `data/ephemeris-2026-2027.json`, inlined into `index.html` at build time
- [x] Corrected KEY_DATES + monthly transit narratives against real computed positions (`tools/generate_content.py`, `tools/generate_months.py`) — caught and fixed several real errors in the old hand-researched dates (e.g. July 2026 New Moon was dated the 24th, actually the 14th; Jupiter's Oct 2026–Jan 2027 detour into Leo/8th house was missing entirely; Mercury Rx Nov 2026 was off by ~2 weeks)
- [x] Live daily transit engine (`getTodayTransits()`) — real conjunction/house detection against Maddie's natal chart, surfaced on the Today card
- [x] New tabs: **Overview** (quick dashboard), **Living Chart** (today's real activations + Story + personalized "how to use this planner" guide + travel/timing tips), **Human Design** (bodygraph + type/authority/profile/channels + HD↔Vedic synthesis), **Cycle + Hormones** (cycle tracker, phase-aware daily card integration, one-month symptom tracker, weekly TCM tongue-check reminder)
- [ ] Roll the same components out to Chloe's, Andie's, Devin's, and Kyle's planners (next round)
- [ ] Send each subscriber "add to home screen" instructions once their planner is updated

**Regenerating the ephemeris data (e.g. for a new date range or a new person):** `cd tools && python3 generate_ephemeris.py && python3 generate_content.py && python3 generate_months.py && python3 splice_content.py && python3 splice_engine.py` (requires `pyswisseph`: `pip install pyswisseph`)

---

## 🔗 Live URLs

| Page | URL | Status |
|------|-----|--------|
| Maddie's Planner | https://eauco-mads.github.io/maddie-planner/ | ✅ Live |
| Chloe's Planner | https://eauco-mads.github.io/chloe-planner/ | ✅ Live |
| Free Planner | https://eauco-mads.github.io/maddie-planner/free.html | ✅ Live |
| Landing Page | https://eauco-mads.github.io/maddie-planner/landing.html | ✅ Live |
| Intake Form | https://eauco-mads.github.io/maddie-planner/intake.html | ✅ Live |
| Thank You + Stripe | https://eauco-mads.github.io/maddie-planner/thankyou.html | ✅ Live |
| Subscriber Sheet | https://docs.google.com/spreadsheets/d/13Et-UBWZSdYLgHNm6qca9B28krauU3euHsIjcVEtZIM | ✅ Live |
| Andie's Planner | https://eauco-mads.github.io/andie-planner/ | ✅ Live |

---

## 💰 Pricing

| Product | Price | Status |
|---------|-------|--------|
| Digital — Monthly | $22.22/month | ✅ Active on Stripe |
| Digital — Annual | ~$197/year | ⏳ Add when 5+ subscribers |
| Physical + Digital | $88–111 one-time + sub | ⏳ Phase 3 |

---

## ✅ Phase 0 — Foundation
> **Completed:** June 22, 2026

- [x] Maddie's personalized planner built + live
- [x] Day-of-week content corrected (June 22–30 fix)
- [x] Chloe's personalized planner built + live
- [x] Intake form built + Formspree connected (`xojoqzro`)
- [x] Thank-you page built + Stripe button live
- [x] Free universal planner (lead magnet) built + live
- [x] Landing page built + live (hero · features · free vs paid · how it works · FAQ · email capture)
- [x] Subscriber tracker Google Sheet created
- [x] PROGRESS.md created in GitHub

---

## 🔄 Phase 1 — Beta
> **Target:** June 22 – July 4, 2026

### Planners
- [x] Chloe filled out intake form — confirmed working ✦
- [x] **Andie (sister)'s planner built** ← Libra Rising · 4:35 AM MDT · Vishakha nakshatra ✦
- [x] Pushed to eauco-mads/andie-planner → live at eauco-mads.github.io/andie-planner

### Email + Automation
- [ ] Write GHL 3-email sequence → `target: June 28` 
  - Email 1: Welcome + free planner link
  - Email 2: What the personalized version includes
  - Email 3: Subscribe CTA + intake form link
- [ ] Swap landing page email capture → GHL endpoint → `after GHL sequence is live`

---

## ⏳ Phase 2 — Launch
> **Target:** Week of July 7, 2026  
> *(after beta planners done + GHL sequence set up)*

### Accounts + Profiles
- [ ] TikTok account created → `July 7`
- [ ] TikTok bio written + profile photo + link → `July 7`
- [ ] Pinterest account created → `July 7`
- [ ] Pinterest boards set up (Astrology · Human Design · Moon · Planner Aesthetic) → `July 7`

### Content
- [ ] 5 TikTok videos filmed (screen record planner + voiceover) → `July 8–10`
  - Video 1: What is this? (show the planner + explain personalized vs free)
  - Video 2: Your moon phases for the year
  - Video 3: Planet day energy — Monday through Sunday
  - Video 4: How it's built (intake → chart → your planner)
  - Video 5: Free planner walkthrough + CTA
- [ ] Pinterest pins made (planner screenshots → landing page) → `July 10`
- [ ] Pick official launch date → `target: July 14, 2026`

### Launch Day
- [ ] First 5 TikToks posted (3-day window around launch) → `July 14–16`
- [ ] Pinterest pins live → `July 14`
- [ ] Post in any existing communities / close network → `July 14`

---

## ⏳ Phase 3 — Subscriber Operations
> **Target:** July 2026 (after first 3–5 paying subscribers)

- [ ] Subscriber onboarding email written (what to expect, how to use the planner)
- [ ] Planner delivery email written (here's your link + how to bookmark it)
- [ ] Zapier: Formspree → Google Sheet auto-fill (free tier = 100 tasks/month)
- [ ] Create `eauco-mads/subscriber-planners` GitHub repo (one folder per person)
- [ ] GHL + Stripe: tag subscribers active/inactive based on payment status

---

## ⏳ Phase 4 — Physical Planners
> **Target:** September 2026

- [ ] Decide on format (spiral bound, perfect bound, hardcover?)
- [ ] Canva design template built — cover + monthly spreads + chart pages
- [ ] Print partner chosen → Mixam (bulk) or Printify (on-demand)
- [ ] Pricing finalized ($88–111 + digital subscription)
- [ ] Annual digital tier added to Stripe (~$197/year)
- [ ] Order form added to landing page
- [ ] First test order placed + reviewed

---

## 👥 Beta Subscribers

| Name | Intake | Planner | Stripe | Notes |
|------|--------|---------|--------|-------|
| Maddie (you) | ✅ | ✅ Live | — | Founder planner |
| Chloe Newby | ✅ | ✅ Live | ⏳ | Beta — Libra Rising |
| Andie Galloway (sister) | ✅ | ✅ Live | ⏳ | Libra Rising · 4:35 AM · Aug 4 2003 · eauco-mads.github.io/andie-planner |

---

## 📋 Workflow — Intake → Planner → Delivery

When a new intake email arrives at maddie@elevatealign.com:

1. Paste or forward the intake data to Claude
2. Claude builds the personalized HTML planner (~1 session)
3. Push to GitHub → private link created
4. Add to Google Sheet (link above)
5. Email subscriber their private link
6. Confirm Stripe subscription is active

> Claude cannot read email automatically — Maddie pastes the data each time.

---

## 🛠 What Claude Needs to Build a New Planner

1. Full name
2. Birth date (day / month / year)
3. Birth time + accuracy (exact / approximate / unknown)
4. Birth city + country
5. HD type + authority (if provided)
6. Aesthetic preferences / color notes / vibe
7. Focus areas for the year

Tell Claude: *"Build a personalized planner in the style of Maddie's planner — see PROGRESS.md for architecture."*

---

## 🔑 Key Info

| Thing | Detail |
|-------|--------|
| Formspree endpoint | `xojoqzro` → maddie@elevatealign.com |
| Stripe link | https://buy.stripe.com/bJe3cwfhgfX68gE98I4ow01 |
| Git repo | `eauco-mads/maddie-planner` |
| Local clone | `/tmp/maddie-planner/` |
| Planner local file | `/Users/maddiegalloway/Desktop/Claude/Maddie_Daily_Planner_2026-2027.html` |
| Design system | Cormorant Garamond + Inter · teal `#066664` · peach `#FDBB89` · gold `#B8832A` |
| Vedic system | Jyotish · Lahiri Ayanamsha · Whole Sign Houses |
