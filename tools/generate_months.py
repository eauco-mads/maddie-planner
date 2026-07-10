#!/usr/bin/env python3
"""
Regenerates MONTHS[].vedic.transits/overview using real ephemeris data.

Key correction vs the old hand-written file: Jupiter does NOT stay in Cancer
(7th house) continuously through the year. Real transit: Cancer (Jun 2 2026) ->
Leo/8th (Oct 31 2026) -> back to Cancer/7th retrograde (Jan 25 2027) -> Leo/8th
for good (Jun 26 2027). The old file said Jupiter stayed in Cancer the entire
year until June 2027 -- materially wrong for Oct 2026-Jan 2027.

Run: python3 tools/generate_months.py
Output: data/months_vedic.js, data/months_vedic.json
"""
import json

with open('data/ephemeris-2026-2027.json') as f:
    EPH = json.load(f)
with open('data/key_dates.js') as f:
    pass  # key dates already regenerated separately; this pulls straight from EPH

MONTH_IDS = ['2026-06','2026-07','2026-08','2026-09','2026-10','2026-11','2026-12',
             '2027-01','2027-02','2027-03','2027-04','2027-05','2027-06','2027-07']
MONTH_NAMES = {'06':'June','07':'July','08':'August','09':'September','10':'October',
               '11':'November','12':'December','01':'January','02':'February','03':'March','04':'April','05':'May'}

HOUSE_NAME = {1:'1st house (identity, your Rising sign)',2:'2nd house (self-worth, values, voice)',
              3:'3rd house (communication, expression)',4:'4th house (home, inner foundation)',
              5:'5th house (creativity, joy — your natal Moon/Jupiter/Saturn stellium)',
              6:'6th house (daily life, health, service — Rahu\'s natal house)',
              7:'7th house (partnership, collaboration)',
              8:'8th house (depth, transformation, hidden resources — your natal Mars\'s house)',
              9:'9th house (dharma, philosophy, higher direction)',
              10:'10th house (career, public reputation — your natal Sun/Mercury)',
              11:'11th house (community, income — your natal Venus)',
              12:'12th house (inner life, release — Ketu\'s natal house)'}

DASHA_MEANING = {'Jupiter':'wisdom, grace, expansion, dharma','Saturn':'discipline, endurance, structures that last',
                  'Mercury':'communication, precision, message','Venus':'devotion, beauty, relationship',
                  'Rahu':'karmic acceleration, unconventional growth'}

HOUSE_COLOR = {
    1:'your Rising sign itself — Uttara Ashadha, the nakshatra of the long, earned victory',
    2:'the house Saturn (your chart ruler) governs by rulership — what you believe you\'re worth',
    5:'the house your natal Moon, Jupiter, and Saturn all share — the dominant signature of your entire chart',
    6:'Rahu\'s natal house — your karmic growth edge runs through daily work, health, and unglamorous service',
    7:'the house with no natal planets of your own, which is exactly why a guest as significant as exalted Jupiter can redecorate it so completely',
    8:'your natal Mars\'s house (Purva Phalguni) — where your best research and depth-work happens beneath the surface',
    10:'your natal Sun and Mercury\'s house — Budha-Aditya Yoga, aesthetic precision meeting a sharp, visible mind',
    11:'your natal Venus\'s house (Anuradha) — devotion and loyalty that compounds slowly rather than networking that moves fast',
    12:'Ketu\'s natal house (Purva Ashadha) — deep past-life spiritual reserve, always available beneath the noise',
}


def dasha_context_for(date):
    for maha in EPH['dasha']:
        if maha['start'][:10] <= date <= maha['end'][:10]:
            for anta in maha['antardashas']:
                if anta['start'][:10] <= date <= anta['end'][:10]:
                    return maha['mahadasha'], anta['antardasha']
    return None, None


def ordinal_(n):
    return {1:'1st',2:'2nd',3:'3rd',4:'4th',5:'5th',6:'6th',7:'7th',8:'8th',9:'9th',10:'10th',11:'11th',12:'12th'}[n]


def month_events(mo):
    out = {'lunations': [], 'eclipses': [], 'stations': []}
    for l in EPH['lunations']:
        if l['iso'][:7] == mo:
            out['lunations'].append(l)
    for e in EPH['eclipses']:
        if e['iso'][:7] == mo:
            out['eclipses'].append(e)
    for s in EPH['stations']:
        if s['iso'][:7] == mo:
            out['stations'].append(s)
    return out


def main():
    result = {}
    for mo in MONTH_IDS:
        days = sorted(d for d in EPH['daily'] if d.startswith(mo))
        first_day, last_day = days[0], days[-1]
        jup_first, jup_last = EPH['daily'][first_day]['jupiter'], EPH['daily'][last_day]['jupiter']
        rahu_first = EPH['daily'][first_day]['rahu']
        ketu_first = EPH['daily'][first_day]['ketu']
        sat_first = EPH['daily'][first_day]['saturn']
        maha, anta = dasha_context_for(first_day)

        transits = []
        if jup_first['sign'] != jup_last['sign']:
            transits.append(f"Jupiter shifts from {jup_first['sign']} ({HOUSE_NAME[jup_first['house']]}) to {jup_last['sign']} ({HOUSE_NAME[jup_last['house']]}) this month")
        else:
            exalt = ' — EXALTED, maximum strength' if jup_first['sign'] == 'Cancer' else ''
            transits.append(f"Jupiter in {jup_first['sign']} — {HOUSE_NAME[jup_first['house']]}{exalt}")
        if maha:
            transits.append(f"{maha}" + (f"-{anta}" if anta else '') + f" Antardasha active ({DASHA_MEANING.get(maha,'')})")
        transits.append(f"Saturn {'(R) ' if sat_first['retrograde'] else ''}in {sat_first['sign']} — {HOUSE_NAME[sat_first['house']]}")
        transits.append(f"Rahu in {rahu_first['sign']} — {HOUSE_NAME[rahu_first['house']]} / Ketu in {ketu_first['sign']} — {HOUSE_NAME[ketu_first['house']]}")

        ev = month_events(mo)
        for l in ev['lunations']:
            d = l['iso'][8:10]
            kind = 'New Moon' if l['type']=='new_moon' else 'Full Moon'
            transits.append(f"{kind} {MONTH_NAMES[mo[5:7]]} {int(d)} in {l['sign_sidereal']} — {HOUSE_NAME[l['house']]}")
        for e in ev['eclipses']:
            d = e['iso'][8:10]
            kind = 'Solar Eclipse' if e['type']=='solar_eclipse' else 'Lunar Eclipse'
            transits.append(f"★ {kind} {MONTH_NAMES[mo[5:7]]} {int(d)} in {e['sign_sidereal']} — {HOUSE_NAME[e['house']]}")
        for s in ev['stations']:
            d = s['iso'][8:10]
            transits.append(f"{s['planet'].capitalize()} {'stations retrograde' if s['direction']=='retrograde' else 'goes direct'} {MONTH_NAMES[mo[5:7]]} {int(d)} in {s['sign_sidereal']}")

        # Overview paragraph
        pieces = []
        jhouse_first_desc = HOUSE_COLOR.get(jup_first['house'], HOUSE_NAME[jup_first['house']].split('(')[1].rstrip(')'))
        jhouse_last_desc = HOUSE_COLOR.get(jup_last['house'], HOUSE_NAME[jup_last['house']].split('(')[1].rstrip(')'))
        if jup_first['house'] == 7 and jup_last['house'] == 8:
            pieces.append(f"Jupiter leaves Cancer and enters Leo this month — your 8th house — shifting out of the partnership blessing it's been running since June "
                           f"and into a depth chapter instead. This isn't the final exit (Jupiter retrogrades back into Cancer at the end of January before leaving for good in June 2027), but "
                           f"it's a real, feelable shift into {jhouse_last_desc}.")
        elif jup_first['house'] == 8 and jup_last['house'] == 7:
            pieces.append(f"Jupiter moves back into Cancer this month — retrograding into your 7th house of partnership again after its detour through Leo (8th house, depth/transformation) "
                           f"since late October. The partnership blessing resumes, now carrying whatever the Leo depth-chapter surfaced.")
        elif jup_first['sign'] != jup_last['sign']:
            pieces.append(f"Jupiter changes signs this month, moving from {jup_first['sign']} into {jup_last['sign']} — shifting toward {jhouse_last_desc}.")
        else:
            exalt_note = " at full exalted strength — the most benefic placement Jupiter can hold" if jup_first['sign']=='Cancer' else ''
            pieces.append(f"Jupiter continues through {jup_first['sign']}{exalt_note}, activating {jhouse_first_desc}.")
        if maha:
            pieces.append(f"You're in your {maha} Mahadasha" + (f", {anta} Antardasha" if anta else '') + f" — a chapter shaped by {DASHA_MEANING.get(maha, maha)}" + (f" filtered through {DASHA_MEANING.get(anta,'')}" if anta and anta in DASHA_MEANING else '') + ".")
        if ev['eclipses']:
            e = ev['eclipses'][0]
            e_desc = HOUSE_COLOR.get(e['house'], '')
            pieces.append(f"The {'solar' if e['type']=='solar_eclipse' else 'lunar'} eclipse this month lands in {e['sign_sidereal']} — your {ordinal_(e['house'])} house" + (f", {e_desc}" if e_desc else '') + " — one of the more significant single events of the planner year.")
        elif ev['lunations']:
            standout = max(ev['lunations'], key=lambda l: 1 if l['house'] in (1,5,7,10) else 0)
            kind = 'New Moon' if standout['type']=='new_moon' else 'Full Moon'
            s_desc = HOUSE_COLOR.get(standout['house'], '')
            pieces.append(f"The {kind.lower()} in {standout['sign_sidereal']} activates your {ordinal_(standout['house'])} house" + (f" — {s_desc}" if s_desc else '') + '.')
        if ev['stations']:
            s = ev['stations'][0]
            pieces.append(f"{s['planet'].capitalize()} {'turns retrograde' if s['direction']=='retrograde' else 'turns direct'} this month in {s['sign_sidereal']} — a cue to {'review rather than launch' if s['direction']=='retrograde' else 'act on what became clear during the retrograde'} in your {HOUSE_NAME[s['house']]}.")

        overview = ' '.join(pieces)
        result[mo] = {'transits': transits, 'overview': overview}

    lines = []
    for mo in MONTH_IDS:
        r = result[mo]
        t_list = ",".join("'" + t.replace("'", "\\'") + "'" for t in r['transits'])
        lines.append(f"MONTHS_VEDIC['{mo}'] = {{ transits:[{t_list}], overview:'{r['overview'].replace(chr(39), chr(92)+chr(39))}' }};")

    with open('data/months_vedic.js', 'w') as f:
        f.write('const MONTHS_VEDIC = {};\n' + '\n'.join(lines) + '\n')
    with open('data/months_vedic.json', 'w') as f:
        json.dump(result, f, indent=1)
    print(f"Wrote data/months_vedic.js + .json — {len(result)} months")
    print()
    print("KEY CORRECTION — Jupiter's real path (old file said Cancer/7th ALL year):")
    print(f"  Jun 2 2026: enters Cancer (7th, exalted)")
    print(f"  Oct 31 2026: enters Leo (8th) <- old file missed this entirely")
    print(f"  Jan 25 2027: back to Cancer (7th, retrograde re-entry)")
    print(f"  Jun 26 2027: enters Leo (8th) for good")


if __name__ == '__main__':
    main()
