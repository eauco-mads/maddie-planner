#!/usr/bin/env python3
"""
Generates a real Swiss Ephemeris data file (Lahiri sidereal + whole-sign house
mapping) for Maddie's planner: daily planet positions, exact lunations,
eclipses, retrograde stations, and her Vimshottari Dasha timeline.

Run: python3 tools/generate_ephemeris.py
Output: data/ephemeris-2026-2027.json
"""
import json
import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)

# ── Maddie's birth data (Afton, Wyoming) ─────────────────────────────────────
BIRTH_LAT, BIRTH_LON = 42.7238, -110.9310
BIRTH_UT_HOUR = 15 + 12 / 60 + 6  # Oct 17 2000, 3:12pm MDT (UTC-6) -> UTC hour
BIRTH_JD = swe.julday(2000, 10, 17, BIRTH_UT_HOUR)

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra',
          'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
NAKSHATRAS = ['Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashirsha', 'Ardra',
              'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
              'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
              'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta',
              'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati']
PLANET_CODES = {
    'sun': swe.SUN, 'moon': swe.MOON, 'mercury': swe.MERCURY, 'venus': swe.VENUS,
    'mars': swe.MARS, 'jupiter': swe.JUPITER, 'saturn': swe.SATURN,
}
# Natal Rising sign index (Capricorn = 9) drives whole-sign house mapping for transits.
RISING_SIGN_IDX = SIGNS.index('Capricorn')

DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
DASHA_YEARS = {'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
               'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17}
NAK_LORD = {}
for i, n in enumerate(NAKSHATRAS):
    NAK_LORD[n] = DASHA_ORDER[i % 9]


def ayanamsha(jd):
    return swe.get_ayanamsa_ut(jd)


def sidereal_lon(jd, code):
    trop = swe.calc_ut(jd, code)[0]
    lon, speed = trop[0], trop[3]
    return (lon - ayanamsha(jd)) % 360, speed


def sign_of(lon):
    return SIGNS[int(lon // 30)]


def nakshatra_of(lon):
    span = 360 / 27
    idx = int(lon // span)
    pada = int((lon % span) // (span / 4)) + 1
    return NAKSHATRAS[idx], pada


def whole_sign_house(planet_sign):
    return (SIGNS.index(planet_sign) - RISING_SIGN_IDX) % 12 + 1


def planet_snapshot(jd):
    out = {}
    for name, code in PLANET_CODES.items():
        lon, speed = sidereal_lon(jd, code)
        trop_lon = (lon + ayanamsha(jd)) % 360
        sign = sign_of(lon)
        nak, pada = nakshatra_of(lon)
        out[name] = {
            'lon': round(lon, 4), 'sign': sign, 'deg': round(lon % 30, 2),
            'sign_tropical': sign_of(trop_lon),
            'nakshatra': nak, 'pada': pada, 'house': whole_sign_house(sign),
            'retrograde': speed < 0,
        }
    rahu_lon, rahu_speed = sidereal_lon(jd, swe.MEAN_NODE)
    ketu_lon = (rahu_lon + 180) % 360
    for name, lon, speed in (('rahu', rahu_lon, rahu_speed), ('ketu', ketu_lon, -rahu_speed)):
        trop_lon = (lon + ayanamsha(jd)) % 360
        sign = sign_of(lon)
        nak, pada = nakshatra_of(lon)
        out[name] = {
            'lon': round(lon, 4), 'sign': sign, 'deg': round(lon % 30, 2),
            'sign_tropical': sign_of(trop_lon),
            'nakshatra': nak, 'pada': pada, 'house': whole_sign_house(sign),
            'retrograde': True,
        }
    return out


def jd_to_iso(jd):
    y, m, d, h = swe.revjul(jd)
    hh = int(h)
    mm = int(round((h - hh) * 60))
    if mm == 60:
        mm = 0
        hh += 1
    return f"{y:04d}-{m:02d}-{d:02d}T{hh:02d}:{mm:02d}Z"


def daterange_jds(start_jd, end_jd, step=1.0):
    jd = start_jd
    while jd <= end_jd:
        yield jd
        jd += step


def find_lunations(start_jd, end_jd):
    """Find exact New Moon / Full Moon UTC moments by bisecting on Sun-Moon elongation."""
    events = []

    def elong(jd):
        sun = swe.calc_ut(jd, swe.SUN)[0][0]
        moon = swe.calc_ut(jd, swe.MOON)[0][0]
        return (moon - sun) % 360

    prev_jd = start_jd
    prev_e = elong(prev_jd)
    step = 0.5
    jd = start_jd + step
    while jd <= end_jd:
        e = elong(jd)
        for target, label in ((0, 'new_moon'), (180, 'full_moon')):
            prev_diff = (prev_e - target + 180) % 360 - 180
            cur_diff = (e - target + 180) % 360 - 180
            if prev_diff != 0 and (prev_diff < 0) != (cur_diff < 0) and abs(prev_diff) < 90:
                lo, hi = prev_jd, jd
                for _ in range(40):
                    mid = (lo + hi) / 2
                    d = (elong(mid) - target + 180) % 360 - 180
                    if (d < 0) == (prev_diff < 0):
                        lo = mid
                    else:
                        hi = mid
                exact = (lo + hi) / 2
                moon_sid, _ = sidereal_lon(exact, swe.MOON)
                moon_trop = swe.calc_ut(exact, swe.MOON)[0][0]
                events.append({
                    'type': label, 'jd': exact, 'iso': jd_to_iso(exact),
                    'sign_tropical': sign_of(moon_trop),
                    'sign_sidereal': sign_of(moon_sid),
                    'house': whole_sign_house(sign_of(moon_sid)),
                })
        prev_jd, prev_e = jd, e
        jd += step
    return events


def find_eclipses(start_jd, end_jd):
    events = []
    jd = start_jd
    while True:
        try:
            res = swe.sol_eclipse_when_glob(jd, swe.FLG_SWIEPH, 0, False)
        except Exception:
            break
        tret = res[1]
        peak_jd = tret[0]
        if peak_jd > end_jd:
            break
        moon_sid, _ = sidereal_lon(peak_jd, swe.MOON)
        events.append({'type': 'solar_eclipse', 'jd': peak_jd, 'iso': jd_to_iso(peak_jd),
                        'sign_sidereal': sign_of(moon_sid), 'house': whole_sign_house(sign_of(moon_sid))})
        jd = peak_jd + 1
    jd = start_jd
    while True:
        try:
            res = swe.lun_eclipse_when(jd, swe.FLG_SWIEPH, 0, False)
        except Exception:
            break
        tret = res[1]
        peak_jd = tret[0]
        if peak_jd > end_jd:
            break
        moon_sid, _ = sidereal_lon(peak_jd, swe.MOON)
        events.append({'type': 'lunar_eclipse', 'jd': peak_jd, 'iso': jd_to_iso(peak_jd),
                        'sign_sidereal': sign_of(moon_sid), 'house': whole_sign_house(sign_of(moon_sid))})
        jd = peak_jd + 1
    events.sort(key=lambda e: e['jd'])
    return events


def find_stations(start_jd, end_jd):
    """Detect retrograde/direct stations for Mercury, Venus, Mars, Jupiter, Saturn."""
    stations = []
    for name, code in (('mercury', swe.MERCURY), ('venus', swe.VENUS), ('mars', swe.MARS),
                        ('jupiter', swe.JUPITER), ('saturn', swe.SATURN)):
        prev_jd = start_jd
        prev_speed = swe.calc_ut(prev_jd, code)[0][3]
        jd = start_jd + 1
        while jd <= end_jd:
            speed = swe.calc_ut(jd, code)[0][3]
            if (prev_speed < 0) != (speed < 0):
                lo, hi = prev_jd, jd
                for _ in range(40):
                    mid = (lo + hi) / 2
                    s = swe.calc_ut(mid, code)[0][3]
                    if (s < 0) == (prev_speed < 0):
                        lo = mid
                    else:
                        hi = mid
                exact = (lo + hi) / 2
                lon_sid, _ = sidereal_lon(exact, code)
                stations.append({
                    'planet': name, 'jd': exact, 'iso': jd_to_iso(exact),
                    'direction': 'retrograde' if speed < 0 else 'direct',
                    'sign_sidereal': sign_of(lon_sid),
                    'house': whole_sign_house(sign_of(lon_sid)),
                })
            prev_jd, prev_speed = jd, speed
            jd += 1
    stations.sort(key=lambda s: s['jd'])
    return stations


def vimshottari_dasha(natal_jd, natal_moon_lon, span_start_jd, span_end_jd):
    """Compute Mahadasha + Antardasha periods overlapping [span_start_jd, span_end_jd]."""
    span = 360 / 27
    nak_idx = int(natal_moon_lon // span)
    nak_name = NAKSHATRAS[nak_idx]
    start_lord = NAK_LORD[nak_name]
    frac_into_nak = (natal_moon_lon % span) / span
    remaining_frac = 1 - frac_into_nak

    lord_i = DASHA_ORDER.index(start_lord)
    balance_years = DASHA_YEARS[start_lord] * remaining_frac

    periods = []
    cursor_jd = natal_jd
    first_maha_years = balance_years
    periods.append((start_lord, cursor_jd, cursor_jd + first_maha_years * 365.2425))
    cursor_jd += first_maha_years * 365.2425
    i = lord_i
    while cursor_jd < span_end_jd + 3000:
        i = (i + 1) % 9
        lord = DASHA_ORDER[i]
        dur = DASHA_YEARS[lord] * 365.2425
        periods.append((lord, cursor_jd, cursor_jd + dur))
        cursor_jd += dur

    def antardashas(maha_lord, maha_start, maha_end):
        total_years = DASHA_YEARS[maha_lord]
        maha_span_days = maha_end - maha_start
        sub = []
        idx = DASHA_ORDER.index(maha_lord)
        c = maha_start
        for k in range(9):
            sub_lord = DASHA_ORDER[(idx + k) % 9]
            sub_years = DASHA_YEARS[sub_lord]
            sub_dur_days = maha_span_days * (sub_years / 120)
            sub.append((sub_lord, c, c + sub_dur_days))
            c += sub_dur_days
        return sub

    result = []
    for lord, s, e in periods:
        if e < span_start_jd or s > span_end_jd:
            continue
        entry = {
            'mahadasha': lord, 'start': jd_to_iso(s), 'end': jd_to_iso(e),
            'antardashas': [],
        }
        for sub_lord, ss, se in antardashas(lord, s, e):
            if se < span_start_jd or ss > span_end_jd:
                continue
            entry['antardashas'].append({
                'antardasha': sub_lord, 'start': jd_to_iso(ss), 'end': jd_to_iso(se),
            })
        result.append(entry)
    return result


def main():
    start_jd = swe.julday(2026, 5, 25)
    end_jd = swe.julday(2027, 8, 5)

    daily = {}
    jd = start_jd
    while jd <= end_jd:
        y, m, d, _ = swe.revjul(jd)
        # snapshot at 12:00 UTC for a stable "day" reading
        noon_jd = swe.julday(y, m, d, 12.0)
        date_key = f"{y:04d}-{m:02d}-{d:02d}"
        snap = planet_snapshot(noon_jd)
        sun_lon = swe.calc_ut(noon_jd, swe.SUN)[0][0]
        moon_lon = swe.calc_ut(noon_jd, swe.MOON)[0][0]
        elongation = (moon_lon - sun_lon) % 360
        snap['moon_elongation'] = round(elongation, 2)
        daily[date_key] = snap
        jd += 1

    lunations = find_lunations(start_jd, end_jd)
    eclipses = find_eclipses(start_jd, end_jd)
    stations = find_stations(start_jd, end_jd)
    natal_moon_sid, _ = sidereal_lon(BIRTH_JD, swe.MOON)
    dasha = vimshottari_dasha(BIRTH_JD, natal_moon_sid, start_jd, end_jd)

    out = {
        'meta': {
            'system': 'Lahiri sidereal, whole-sign houses from Capricorn Rising',
            'generated_range': [jd_to_iso(start_jd), jd_to_iso(end_jd)],
            'natal_rising': 'Capricorn',
        },
        'daily': daily,
        'lunations': [{k: v for k, v in ev.items() if k != 'jd'} for ev in lunations],
        'eclipses': [{k: v for k, v in ev.items() if k != 'jd'} for ev in eclipses],
        'stations': [{k: v for k, v in ev.items() if k != 'jd'} for ev in stations],
        'dasha': dasha,
    }

    import os
    os.makedirs('data', exist_ok=True)
    with open('data/ephemeris-2026-2027.json', 'w') as f:
        json.dump(out, f, separators=(',', ':'))
    print(f"Wrote data/ephemeris-2026-2027.json — {len(daily)} days, "
          f"{len(lunations)} lunations, {len(eclipses)} eclipses, {len(stations)} stations, "
          f"{len(dasha)} dasha periods")


if __name__ == '__main__':
    main()
