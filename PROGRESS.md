# EAUCO Personalized Planner — Project Progress

> Last updated: June 22, 2026  
> This file is the source of truth. Update it every session.

---

## Live URLs

| What | URL |
|------|-----|
| Maddie's planner | https://eauco-mads.github.io/maddie-planner/ |
| Chloe's planner | https://eauco-mads.github.io/chloe-planner/ |
| Free planner (lead magnet) | https://eauco-mads.github.io/maddie-planner/free.html |
| Intake form | https://eauco-mads.github.io/maddie-planner/intake.html |
| Thank-you + Stripe page | https://eauco-mads.github.io/maddie-planner/thankyou.html |
| Subscriber tracker (Google Sheet) | https://docs.google.com/spreadsheets/d/13Et-UBWZSdYLgHNm6qca9B28krauU3euHsIjcVEtZIM |

## Key Integrations

| Service | What it does | Status |
|---------|-------------|--------|
| Formspree `xojoqzro` | Emails intake submissions to maddie@elevatealign.com | ✅ Live |
| Stripe | $22.22/month subscription | ✅ Live — link on thank-you page |
| GitHub Pages | Hosts all HTML files | ✅ Live |
| Google Drive MCP | Connected — Drive accessible in Claude sessions | ✅ Active |

## Git Repo

- **Repo:** `eauco-mads/maddie-planner` (main branch)
- **Local clone for pushing:** `/tmp/maddie-planner/`
- **Files in repo:** `index.html`, `free.html`, `intake.html`, `thankyou.html`, `PROGRESS.md`
- **To push updates:** copy file to `/tmp/maddie-planner/`, commit, push

---

## Status by Phase

### ✅ Phase 0 — Foundation (DONE)
- [x] Maddie's personalized planner — live + day-of-week corrected (June 22–30 fix pushed June 22)
- [x] Chloe's planner — live
- [x] Intake form — live + Formspree connected
- [x] Thank-you page — live + Stripe $22.22/month button
- [x] Free planner (lead magnet) — live at /free.html
- [x] Subscriber tracker Google Sheet — created in Drive
- [x] This PROGRESS.md — created

### 🔄 Phase 1 — Beta & Pre-Launch (IN PROGRESS)
- [ ] **Sister fills out intake** — form sent, awaiting response
- [ ] **Chloe fills out intake** — to send
- [ ] **Andie fills out intake** — to send
- [ ] **Sister's planner built** — needs birth data from intake
- [ ] **Free planner polished** — live but needs:
  - [ ] Dedicated repo/URL (suggest: create `eauco-mads/planner` repo → eauco-mads.github.io/planner)
  - [ ] Landing page wrapping it (headline, how it works, CTA to subscribe)
- [ ] **Landing page built** — copy + build needed
- [ ] **Free lead magnet** — decided: free planner IS the lead magnet ✓
- [ ] **GHL email sequence** — 3 emails: deliver free planner → what personalized includes → subscribe CTA

### ⏳ Phase 2 — Launch (NEXT)
- [ ] TikTok account set up + bio
- [ ] Pinterest account set up + boards
- [ ] TikTok content filmed (5 videos — show planner in action)
- [ ] Pinterest pins (planner screenshots → landing page)
- [ ] Launch date picked (suggest: 7-10 days after beta planners done)
- [ ] All 5 TikToks posted in first 3 days

### ⏳ Phase 3 — Subscriber Operations (AFTER LAUNCH)
- [ ] Formspree → Google Sheet auto-connection (options: Zapier free tier OR manual for now)
- [ ] Subscriber onboarding email template written
- [ ] Planner delivery email template written
- [ ] `eauco-mads/subscriber-planners` repo set up (one folder per subscriber)
- [ ] GHL + Stripe integration for active/inactive tagging

### ⏳ Phase 4 — Physical Planners (2-3 months out)
- [ ] Canva design template built
- [ ] Print partner chosen (Mixam for bulk, Printify for on-demand)
- [ ] Pricing set ($88–111 suggested)
- [ ] Order form added to landing page

---

## Workflow: Intake → Planner → Delivery

When a new intake email arrives at maddie@elevatealign.com:

1. **Forward/paste the intake data** to Claude in a new session
2. Claude pulls birth chart (Vedic + Western + HD) and **builds personalized HTML planner**
3. Save the HTML file, push to GitHub (either in subscriber-planners repo or maddie-planner/subscribers/)
4. **Add subscriber to Google Sheet** (link above) — fill in all columns
5. **Send delivery email** with their private planner link
6. Confirm Stripe subscription is active

---

## Intake Form Fields (what Formspree emails contain)

- Full name + email
- Birth date, time, time accuracy (exact/approximate/unknown)
- Birth city + country
- Vedic rising + Western sun (if known)
- HD type, authority, profile (optional)
- Vibe checkboxes + color notes
- Focus areas for the year
- Additional notes

---

## What Claude Needs to Build a New Planner

(Share this in any new session before asking for a build)

1. Full name
2. Birth date (day/month/year)
3. Birth time (and accuracy)
4. Birth city + country
5. HD type + authority (if provided)
6. Aesthetic preferences / color notes
7. Focus areas

Then say: "Build a personalized planner in the style of Maddie's planner at eauco-mads.github.io/maddie-planner — see PROGRESS.md for architecture and reference files."

---

## Subscriber Tracker

**Google Sheet:** https://docs.google.com/spreadsheets/d/13Et-UBWZSdYLgHNm6qca9B28krauU3euHsIjcVEtZIM

Columns: Name · Email · Submission Date · Birth Date · Birth Time · Time Accuracy · Birth City · Birth Country · Vedic Rising · HD Type · HD Authority · HD Profile · Vibe · Color Notes · Focus Areas · Notes · Planner Status · Planner URL · Planner Built Date · Stripe Status · Subscription Start · Monthly Amount · Notes

---

## Key People

| Person | Role | Status |
|--------|------|--------|
| Maddie | You — founder, first planner live | ✅ |
| Chloe Newby | Beta tester — planner live | ✅ |
| Maddie's sister | Beta tester #2 — intake sent | 🔄 Awaiting form |
| Andie | Beta tester — to send form | ⏳ |

---

## Pricing

- **Digital subscription:** $22.22/month
- **Annual (future):** ~$197/year (suggest after 5+ subscribers)
- **Physical planner (future):** $88–111 + digital access

---

## Important Notes

- Formspree submissions email to: maddie@elevatealign.com
- Claude CANNOT read emails automatically — Maddie must forward/paste intake data
- To auto-connect Formspree → Google Sheet: use Zapier free tier (100 tasks/month free)
- All planner files use same CSS design system — see Maddie's planner as the master reference
- Capricorn Rising correction was made in session — all house assignments now accurate
- June 22–30 day-of-week content corrected June 22, 2026
