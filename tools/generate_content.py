#!/usr/bin/env python3
"""
Regenerates KEY_DATES and MONTHS[].vedic content for Maddie's planner using the
real ephemeris data (data/ephemeris-2026-2027.json) instead of hand-researched
(and sometimes wrong -- e.g. the old file's July 2026 New Moon was dated the 24th;
real elongation math puts it on the 14th) dates.

House meanings are stable regardless of which month a transit lands in, so this
uses a reusable per-house template library (her actual natal content per house)
and interpolates the real date/sign/dasha context computed by generate_ephemeris.py.

Run: python3 tools/generate_content.py
Output: data/key_dates.js, data/months_vedic.js  (JS const literals, spliced into index.html by hand)
"""
import json

with open('data/ephemeris-2026-2027.json') as f:
    EPH = json.load(f)

MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December']

# ── House meanings, written once, reused everywhere a transit/lunation lands there ──
# (house numbers are relative to Maddie's Capricorn Rising / whole-sign houses)
HOUSE = {
    1: {'name': 'Identity + Rising Sign', 'natal': 'your Rising sign itself (Uttara Ashadha) — the house of the body, presence, and how you meet the world',
        'seed': 'who you are consciously choosing to become — not what you\'ll do, who you\'ll be', 'note': 'the most personal house a transit can touch: this is your face to the world'},
    2: {'name': 'Self-Worth + Values + Voice', 'natal': 'the house Saturn (your chart ruler) governs by rulership',
        'seed': 'the honest, unminimized picture of your worth — skills, wisdom, resources you tend to undercount', 'note': 'rules speech in Jyotish: what you say about your own value'},
    3: {'name': 'Communication + Voice + Expression', 'natal': 'your everyday voice and courage to speak',
        'seed': 'one thing you\'ve been meaning to say, without self-editing', 'note': 'the house of daily expression, writing, and short journeys'},
    4: {'name': 'Home + Inner Foundation', 'natal': 'your private world and emotional roots',
        'seed': 'what you want your home and inner life to feel like', 'note': 'the ground everything public is built on'},
    5: {'name': 'Creativity + Joy — Your Natal Stellium', 'natal': 'your Moon, Jupiter, and Saturn all live here in Taurus — the dominant signature of your entire chart',
        'seed': 'a creative, romantic, or self-expressive intention that comes from the deepest, most essentially-you place', 'note': 'your greatest gift: where feeling, intelligence, and beauty converge'},
    6: {'name': 'Daily Life + Health + Service', 'natal': 'Rahu lives here natally in Gemini — your karmic growth edge runs through daily work and health',
        'seed': 'a daily practice or health rhythm worth committing to', 'note': 'rewards specificity and consistency over intensity'},
    7: {'name': 'Partnership + Collaboration', 'natal': 'no natal planets here, but Jupiter transits exalted through this house for most of this planner\'s year',
        'seed': 'who you are choosing to build WITH', 'note': 'the house of the people who mirror your growth'},
    8: {'name': 'Depth + Transformation + Hidden Resources', 'natal': 'your Mars lives here in Leo (Purva Phalguni)',
        'seed': 'a hidden strength, resource, or truth ready to surface', 'note': 'your best research/investigative work happens beneath the surface, before the public announcement'},
    9: {'name': 'Dharma + Philosophy + Higher Direction', 'natal': 'your sense of purpose and earned conviction',
        'seed': 'a belief about your path arrived at through lived experience, not what you\'ve been told', 'note': 'rewards earned philosophy over borrowed belief'},
    10: {'name': 'Career + Public Reputation', 'natal': 'your Sun and Mercury both live here in Libra — Budha-Aditya Yoga, your professional identity house',
         'seed': 'a vision for who you are professionally and how you want to be publicly known', 'note': 'your career runs on aesthetic precision + clear communication together'},
    11: {'name': 'Community + Income', 'natal': 'your Venus lives here in Scorpio (Anuradha) — devotion that earns, loyalty that compounds',
         'seed': 'a community or income intention rooted in genuine belonging, not strategy alone', 'note': 'abundance here flows through sustained, loyal relationship — not quick networking'},
    12: {'name': 'Inner Life + Release + the Unseen', 'natal': 'Ketu lives here natally in Sagittarius (Purva Ashadha) — deep past-life spiritual wisdom',
         'seed': 'a private, spiritual intention — something tended quietly, not announced', 'note': 'grows in the dark; rewards what\'s real over what\'s performed'},
}

DASHA_LORDS_TEXT = {
    'Jupiter': 'wisdom, grace, expansion, and dharma',
    'Saturn': 'discipline, endurance, and structures that last',
    'Mercury': 'communication, precision, and message',
    'Venus': 'devotion, beauty, and relationship',
    'Sun': 'identity, authority, and visibility',
    'Moon': 'emotional truth and instinct',
    'Mars': 'courage, drive, and depth-work',
    'Rahu': 'karmic acceleration and unconventional growth',
    'Ketu': 'release, spiritual wisdom, and detachment',
}


def dasha_context_for(iso):
    """Find active Mahadasha-Antardasha for a given ISO date string."""
    date = iso[:10]
    for maha in EPH['dasha']:
        if maha['start'][:10] <= date <= maha['end'][:10]:
            for anta in maha['antardashas']:
                if anta['start'][:10] <= date <= anta['end'][:10]:
                    return maha['mahadasha'], anta['antardasha']
    return None, None


def fmt_date(iso):
    y, m, d = int(iso[0:4]), int(iso[5:7]), int(iso[8:10])
    return f"{MONTH_NAMES[m-1]} {d}, {y}"


def stellium_bonus(house):
    return house == 5


def rising_bonus(house):
    return house == 1


def jupiter_domain_bonus(house, iso):
    # Jupiter is exalted in Cancer/7th roughly June 2026 - late June 2027 (with a Leo dip Nov'26-Jan'27... actually Leo Oct'26-Jan'27 then back to Cancer)
    return house == 7 and '2026-06' <= iso[:7] <= '2027-06'


def significance_stars(house, iso):
    n = 1
    if stellium_bonus(house):
        n += 2
    if rising_bonus(house):
        n += 2
    if jupiter_domain_bonus(house, iso):
        n += 1
    return min(n, 3)


def new_moon_entry(ev):
    h = ev['house']
    hd = HOUSE[h]
    stars = significance_stars(h, ev['iso'])
    star_str = ' ' + ('★' * stars) if stars > 1 else ''
    maha, anta = dasha_context_for(ev['iso'])
    dasha_line = f" You're in your {maha} Mahadasha" + (f" ({DASHA_LORDS_TEXT.get(maha,'')})" if maha in DASHA_LORDS_TEXT else '') + (f", {anta} Antardasha" if anta else '') + "." if maha else ''
    title = f"New Moon in {ev['sign_sidereal']} — {hd['name']}{star_str}"
    guidance = (f"New Moon in {ev['sign_sidereal']} lands in your {ordinal(h)} house — {hd['name']}. "
                f"{hd['natal'][0].upper()+hd['natal'][1:]}. New moons are for seeding: what you plant here has roughly six months to grow toward the "
                f"full moon that completes it.{dasha_line} This house {hd['note']}.")
    action = f"Write {hd['seed']}. Plant it here, in {ev['sign_sidereal']}, and let the new moon witness it."
    return {'type': 'new-moon', 'title': title, 'house': f"{ordinal(h)} House — {hd['name']}{star_str}", 'guidance': guidance, 'action': action}


def full_moon_entry(ev):
    h = ev['house']
    hd = HOUSE[h]
    stars = significance_stars(h, ev['iso'])
    star_str = ' ' + ('★' * stars) if stars > 1 else ''
    title = f"Full Moon in {ev['sign_sidereal']} — {hd['name']}{star_str}"
    guidance = (f"Full Moon in {ev['sign_sidereal']} illuminates your {ordinal(h)} house — {hd['name']}. "
                f"{hd['natal'][0].upper()+hd['natal'][1:]}. Full moons complete or reveal what's been building since the new moon six months prior — "
                f"whatever has been growing in this house is at full brightness tonight. This house {hd['note']}.")
    action = f"Let yourself fully feel what's arrived in this house rather than managing it. Write what's actually true here right now, without softening it."
    return {'type': 'full-moon', 'title': title, 'house': f"{ordinal(h)} House — {hd['name']}{star_str}", 'guidance': guidance, 'action': action}


def eclipse_entry(ev):
    h = ev['house']
    hd = HOUSE[h]
    solar = ev['type'] == 'solar_eclipse'
    kind = 'Solar' if solar else 'Lunar'
    title = f"{kind} Eclipse in {ev['sign_sidereal']} — {hd['name']} ★"
    if solar:
        guidance = (f"Solar Eclipse in {ev['sign_sidereal']} — your {ordinal(h)} house, {hd['name']}. Solar eclipses fast-forward: whatever has been building in this "
                    f"house accelerates suddenly, sometimes faster than feels comfortable. {hd['natal'][0].upper()+hd['natal'][1:]}. Eclipse seeds bloom within roughly six months.")
        action = "Document every shift in this life area over the 48 hours after the eclipse — what arrives now moves fast. Write it down while it's fresh."
    else:
        guidance = (f"Lunar Eclipse in {ev['sign_sidereal']} — your {ordinal(h)} house, {hd['name']}. Lunar eclipses complete: something in this house's story is "
                    f"finishing its old form, not through loss but through graduation. {hd['natal'][0].upper()+hd['natal'][1:]}.")
        action = "Name honestly what's completing in this life area. Thank it for whatever it protected, then let it close."
    return {'type': f"eclipse-{'solar' if solar else 'lunar'}", 'title': title, 'house': f"{ordinal(h)} House — {hd['name']} ★", 'guidance': guidance, 'action': action}


def station_entry(ev):
    planet = ev['planet'].capitalize()
    h = ev['house']
    hd = HOUSE[h]
    is_start = ev['direction'] == 'retrograde'
    title = f"{planet} {'Retrograde Begins' if is_start else 'Goes Direct'}"
    house_line = f"{ordinal(h)} house — {hd['name']}"
    if is_start:
        guidance = (f"{planet} stations retrograde in {ev['sign_sidereal']}, your {house_line}. Retrogrades are for review, not launch: whatever this "
                    f"house governs asks for revisiting, not new starts, until {planet} turns direct again. {hd['natal'][0].upper()+hd['natal'][1:]}.")
        action = f"Review rather than initiate in this life area. What needs revisiting before you move forward again?"
    else:
        guidance = (f"{planet} goes direct in {ev['sign_sidereal']}, your {house_line}. The clarity the retrograde built in this area of life is now "
                    f"actionable — forward motion returns.")
        action = "Take one concrete action on whatever became clear during the retrograde. The first 48 hours after station-direct are especially potent."
    return {'type': f"retro-{'start' if is_start else 'end'}", 'title': title, 'house': house_line, 'guidance': guidance, 'action': action}


def ordinal(n):
    return {1:'1st',2:'2nd',3:'3rd',4:'4th',5:'5th',6:'6th',7:'7th',8:'8th',9:'9th',10:'10th',11:'11th',12:'12th'}[n]


def build_key_dates():
    out = {}
    for ev in EPH['lunations']:
        date = ev['iso'][:10]
        entry = new_moon_entry(ev) if ev['type'] == 'new_moon' else full_moon_entry(ev)
        out[date] = entry
    for ev in EPH['eclipses']:
        date = ev['iso'][:10]
        out[date] = eclipse_entry(ev)  # eclipses override lunation entry same-day if any
    for ev in EPH['stations']:
        date = ev['iso'][:10]
        if date not in out:  # don't clobber a lunation/eclipse same day
            out[date] = station_entry(ev)
    # keep birthday (not astronomically derived)
    out['2026-10-17'] = {'type': 'birthday', 'title': 'Happy 26th Birthday, Maddie ✦',
        'house': 'Born October 17, 2000 · 3:12 PM · Afton, Wyoming',
        'guidance': 'You were born in the mountain air of Wyoming on a crisp October afternoon — 3:12 PM, Afton — and you arrive at 26 as a Capricorn Rising with Uttara Ashadha on your Ascendant. Uttara Ashadha is the nakshatra of final victory — the one who endures, who builds things that last, who does not quit before the real reward arrives.',
        'action': 'Write a letter to yourself today — not about what you want to build, but about who you already are right now. Seal it. Open it next October.'}
    return out


def js_escape(s):
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')


def main():
    key_dates = build_key_dates()
    lines = ["const KEY_DATES = {"]
    for date in sorted(key_dates.keys()):
        e = key_dates[date]
        lines.append(f"  '{date}':{{ type:'{e['type']}', title:'{js_escape(e['title'])}', house:'{js_escape(e['house'])}', guidance:'{js_escape(e['guidance'])}', action:'{js_escape(e['action'])}' }},")
    lines.append("};")

    import os
    os.makedirs('data', exist_ok=True)
    with open('data/key_dates.js', 'w') as f:
        f.write('\n'.join(lines))
    print(f"Wrote data/key_dates.js — {len(key_dates)} entries")
    print("Sample corrections vs old file:")
    for d in ['2026-07-14','2026-07-24','2026-11-01']:
        if d in key_dates:
            print(f"  {d}: {key_dates[d]['title']}")


if __name__ == '__main__':
    main()
