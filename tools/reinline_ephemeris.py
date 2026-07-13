#!/usr/bin/env python3
"""Re-inlines an updated data/ephemeris-2026-2027.json into index.html,
replacing the existing `const EPHEMERIS = {...};` blob in place."""
import re

with open('index.html') as f:
    html = f.read()
with open('data/ephemeris-2026-2027.json') as f:
    eph_json = f.read()

pattern = re.compile(r"const EPHEMERIS = \{.*?\};\n", re.DOTALL)
m = pattern.search(html)
assert m, "EPHEMERIS blob not found"
html = html[:m.start()] + f"const EPHEMERIS = {eph_json};\n" + html[m.end():]

with open('index.html', 'w') as f:
    f.write(html)
print(f"Re-inlined EPHEMERIS ({len(eph_json)} chars)")
