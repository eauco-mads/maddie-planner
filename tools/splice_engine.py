#!/usr/bin/env python3
"""Inlines the ephemeris JSON as a JS const and replaces getMoonData() +
adds a real daily-transit engine, wired to Maddie's natal chart."""
import re

with open('index.html') as f:
    html = f.read()

with open('data/ephemeris-2026-2027.json') as f:
    eph_json = f.read()

# ── 1. Inline EPHEMERIS const right before NM_ANCHORS ──
marker = "const NM_ANCHORS = ["
assert html.count(marker) == 1
inline_block = f"const EPHEMERIS = {eph_json};\n"
html = html.replace(marker, inline_block + marker, 1)

# ── 2. Replace getMoonData() with a real-data version (keeps old NM_ANCHORS as fallback only) ──
old_fn_re = re.compile(r"function getMoonData\(dateStr\)\{.*?\n\}\n", re.DOTALL)
m = old_fn_re.search(html)
assert m, "getMoonData function not found"

new_fn = '''function getMoonData(dateStr){
  const day = EPHEMERIS.daily[dateStr];
  if(!day){
    // outside computed ephemeris range — fall back to approximation
    return getMoonDataApprox(dateStr);
  }
  const moon = day.moon;
  const elong = day.moon_elongation; // 0=new moon, 180=full moon
  const phaseDays = elong/360*29.53;
  let phaseObj = PHASE_NAMES[PHASE_NAMES.length-1];
  for(const p of PHASE_NAMES){ if(phaseDays <= p.max){ phaseObj = p; break; } }
  const vedSign = moon.sign, tropSign = moon.sign_tropical;
  const meaning = MOON_SIGN_MEANINGS[vedSign] || '';
  return { emoji: phaseObj.emoji, phaseName: phaseObj.name, phaseMeaning: phaseObj.meaning,
           tropSign, vedSign, meaning, nakshatra: moon.nakshatra, pada: moon.pada, house: moon.house };
}
function getMoonDataApprox(dateStr){
  const d = new Date(dateStr+'T12:00:00');
  let best = null, bestDiff = Infinity;
  for(const [nmDate] of NM_ANCHORS){
    const nm = new Date(nmDate+'T00:00:00');
    const diff = (d - nm)/86400000;
    if(diff >= 0 && diff < bestDiff){ bestDiff = diff; best = [nmDate, NM_ANCHORS.find(x=>x[0]===nmDate)[1]]; }
  }
  if(!best) return null;
  const daysSinceNM = bestDiff;
  const synodic = 29.53;
  const phase = daysSinceNM % synodic;
  let phaseObj = PHASE_NAMES[PHASE_NAMES.length-1];
  for(const p of PHASE_NAMES){ if(phase <= p.max){ phaseObj = p; break; } }
  const moonLonTrop = (best[1] + daysSinceNM * 13.18) % 360;
  const moonLonVedic = ((moonLonTrop - 24) + 360) % 360;
  const tropSign = ZODIAC_SIGNS_W[Math.floor(moonLonTrop/30)];
  const vedSign  = ZODIAC_SIGNS_V[Math.floor(moonLonVedic/30)];
  const meaning  = MOON_SIGN_MEANINGS[vedSign] || '';
  return { emoji: phaseObj.emoji, phaseName: phaseObj.name, phaseMeaning: phaseObj.meaning, tropSign, vedSign, meaning };
}

// ── REAL DAILY TRANSIT ENGINE ───────────────────────────────────────────────
// Maddie's natal chart (Lahiri sidereal, whole-sign houses, Capricorn Rising)
const NATAL = {
  rising: 'Capricorn',
  sun:     { sign:'Libra',      house:10, nakshatra:'Chitra',        deg:0.93 },
  moon:    { sign:'Taurus',     house:5,  nakshatra:'Mrigashirsha',  deg:28.85 },
  mercury: { sign:'Libra',      house:10, nakshatra:'Vishakha',      deg:21.90 },
  venus:   { sign:'Scorpio',    house:11, nakshatra:'Anuradha',      deg:4.46 },
  mars:    { sign:'Leo',        house:8,  nakshatra:'Purva Phalguni',deg:25.48 },
  jupiter: { sign:'Taurus',     house:5,  nakshatra:'Rohini',        deg:16.80 },
  saturn:  { sign:'Taurus',     house:5,  nakshatra:'Krittika',      deg:6.03 },
  rahu:    { sign:'Gemini',     house:6,  nakshatra:'Punarvasu',     deg:25.79 },
  ketu:    { sign:'Sagittarius',house:12, nakshatra:'Purva Ashadha', deg:25.79 },
};
const HOUSE_HEADLINE = {
  1:'identity and how you\\'re showing up',2:'self-worth and what you believe you\\'re owed',
  3:'communication and daily voice',4:'home and inner foundation',
  5:'your creative core — Moon, Jupiter, and Saturn all live here natally',
  6:'daily work, health, and service — Rahu\\'s natal house',
  7:'partnership and collaboration',8:'depth and transformation — your natal Mars\\'s house',
  9:'dharma and higher direction',10:'career and public reputation — your natal Sun/Mercury',
  11:'community and income — your natal Venus',12:'inner life and release — Ketu\\'s natal house',
};
function dashaContextFor(dateStr){
  for(const maha of (EPHEMERIS.dasha||[])){
    if(maha.start.slice(0,10) <= dateStr && dateStr <= maha.end.slice(0,10)){
      for(const anta of maha.antardashas){
        if(anta.start.slice(0,10) <= dateStr && dateStr <= anta.end.slice(0,10)){
          return { mahadasha: maha.mahadasha, antardasha: anta.antardasha };
        }
      }
    }
  }
  return null;
}
function getTodayTransits(dateStr){
  const day = EPHEMERIS.daily[dateStr];
  if(!day) return null;
  const dasha = dashaContextFor(dateStr);
  const headlines = [];
  // conjunctions: transiting planet within 3° of a natal point, same sign
  const PLANETS = ['sun','moon','mercury','venus','mars','jupiter','saturn','rahu','ketu'];
  for(const p of PLANETS){
    const t = day[p];
    for(const np of PLANETS){
      const natal = NATAL[np];
      if(t.sign === natal.sign && Math.abs(t.deg - natal.deg) <= 3 && p !== np){
        headlines.push(`Transiting ${cap(p)} is conjunct your natal ${cap(np)} in ${t.sign} today — a direct, felt activation.`);
      }
    }
    if(t.retrograde && ['mercury','venus','mars','jupiter','saturn'].includes(p)){
      // retrograde flag alone isn't headline-worthy every day; stations are surfaced via KEY_DATES
    }
  }
  // Moon's house today is the single most-changing, most "today"-relevant signal
  const moonHouse = day.moon.house;
  headlines.push(`Today's Moon is in ${day.moon.sign} (${day.moon.nakshatra}) — your ${ordinal(moonHouse)} house of ${HOUSE_HEADLINE[moonHouse]}.`);
  if(dasha){
    headlines.push(`You're in your ${dasha.mahadasha} Mahadasha, ${dasha.antardasha} Antardasha.`);
  }
  return { headlines, dasha, day };
}
function cap(s){ return s.charAt(0).toUpperCase()+s.slice(1); }
function ordinal(n){ return {1:'1st',2:'2nd',3:'3rd',4:'4th',5:'5th',6:'6th',7:'7th',8:'8th',9:'9th',10:'10th',11:'11th',12:'12th'}[n]||n+'th'; }
'''

html = html[:m.start()] + new_fn + html[m.end():]

with open('index.html', 'w') as f:
    f.write(html)
print(f"Inlined EPHEMERIS ({len(eph_json)} chars) and replaced getMoonData() with real-data engine + getTodayTransits()")
