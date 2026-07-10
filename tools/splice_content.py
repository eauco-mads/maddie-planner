#!/usr/bin/env python3
"""Splices regenerated KEY_DATES and per-month vedic{} blocks into index.html."""
import re
import json

MONTH_IDS = ['2026-06','2026-07','2026-08','2026-09','2026-10','2026-11','2026-12',
             '2027-01','2027-02','2027-03','2027-04','2027-05','2027-06','2027-07']

with open('index.html') as f:
    html = f.read()

# ── Replace KEY_DATES const block ──
with open('data/key_dates.js') as f:
    new_key_dates = f.read().strip()

pattern = re.compile(r"const KEY_DATES = \{.*?\n\};", re.DOTALL)
m = pattern.search(html)
assert m, "KEY_DATES block not found"
html = html[:m.start()] + new_key_dates + html[m.end():]

# ── Replace each month's vedic:{...} line ──
with open('data/months_vedic.json') as f:
    MONTHS_VEDIC = json.load(f)

vedic_line_re = re.compile(r"^(\s*)vedic:\{.*\},$", re.MULTILINE)
lines = html.split('\n')
month_i = 0
for i, line in enumerate(lines):
    if vedic_line_re.match(line):
        mo = MONTH_IDS[month_i]
        data = MONTHS_VEDIC[mo]
        indent = re.match(r"^(\s*)", line).group(1)
        transits_js = ",".join("'" + t.replace("'", "\\'") + "'" for t in data['transits'])
        overview_js = data['overview'].replace("'", "\\'")
        lines[i] = f"{indent}vedic:{{ transits:[{transits_js}], overview:'{overview_js}' }},"
        month_i += 1

assert month_i == 14, f"expected 14 vedic blocks, patched {month_i}"
html = '\n'.join(lines)

with open('index.html', 'w') as f:
    f.write(html)
print(f"Spliced KEY_DATES ({new_key_dates.count(chr(10))+1} lines) and {month_i} month vedic{{}} blocks into index.html")
