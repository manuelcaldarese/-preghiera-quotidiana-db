# Annual DB Update Guide

## When to do this

The current DB covers **2026-01-01 → 2026-12-31**.
Start the update in **November 2026** to leave time for App Store / Play Store review before Jan 1, 2027.

To check the current DB coverage at any time:
```sql
SELECT MIN(date), MAX(date) FROM liturgical_day;
```

---

## What changes vs what stays the same

### Static (do NOT regenerate — already correct)
- `prayer` — traditional prayers
- `psalm` — full psalm texts
- `rosary_mystery` — the 20 mysteries
- `via_crucis` — 14 stations
- `novena` — all novenas
- `feast_calendar` — fixed annual saints
- `saint_greeting` — onomastic greetings

### Regenerate every year (date-dependent)
- `liturgical_day` — new year's seasons, weeks, feast names
- `gospel` — new year's daily Mass readings
- `saint` — new year's daily saints
- `liturgy_proper` — new year's antiphons and collects for lauds/vespers
- `hours_prayer` — new year's full Office texts (psalms, hymns, responsories, etc.)

---

## Step-by-step process

### Step 1 — Create the new DB file

Tell Claude:
```
We need to generate the DB for year YYYY (replace with the new year).
The current DB is data/prayers.db and covers 2026.
Run scripts/build_db.py targeting year YYYY to create a fresh DB with the
new date range. Keep all static tables (prayer, psalm, rosary_mystery,
via_crucis, novena, feast_calendar, saint_greeting) by copying them from
the current DB. Regenerate all date-dependent tables from scratch.
Verify: SELECT MIN(date), MAX(date) FROM liturgical_day; should return
YYYY-01-01 → YYYY-12-31.
```

### Step 2 — Verify what's NULL after the scripts run

Tell Claude:
```
Run this query on data/prayers.db and show me the results:

SELECT
  (SELECT COUNT(*) FROM hours_prayer WHERE responsory IS NULL) as resp_null,
  (SELECT COUNT(*) FROM hours_prayer WHERE invitatory IS NULL AND hour='lauds') as inv_null,
  (SELECT COUNT(*) FROM hours_prayer WHERE benedictus_magnificat IS NULL AND hour IN ('lauds','vespers')) as bm_null,
  (SELECT COUNT(*) FROM hours_prayer WHERE intercessions IS NULL AND hour IN ('lauds','vespers')) as int_null,
  (SELECT COUNT(*) FROM hours_prayer WHERE collect IS NULL AND hour IN ('lauds','terce','vespers')) as col_null,
  (SELECT COUNT(*) FROM liturgy_proper WHERE benedictus_ant IS NULL AND office='lauds') as bant_null,
  (SELECT COUNT(*) FROM liturgy_proper WHERE magnificat_ant IS NULL AND office='vespers') as mant_null;
```

Then tell Claude which columns are still NULL and need to be filled in the following steps.

---

### Step 3 — Fill `hours_prayer.invitatory`

This uses 5 fixed seasonal defaults. Tell Claude:

```
Fill hours_prayer.invitatory for all lauds rows using these seasonal defaults:

ordinary: {
  en: "Come, let us worship the Lord, the king of all creation.",
  it: "Venite, adoriamo il Signore, re dell'universo.",
  es: "Venid, adoremos al Señor, rey de toda la creación."
}
advent: {
  en: "Come, let us worship the Lord, the king who is to come.",
  it: "Venite, adoriamo il Signore, re che deve venire.",
  es: "Venid, adoremos al Señor, rey que ha de venir."
}
christmas: {
  en: "Christ is born for us; come, let us adore him.",
  it: "Cristo è nato per noi: venite, adoriamo.",
  es: "Cristo nos ha nacido; venid, adorémosle."
}
lent: {
  en: "Come, let us worship Christ the Lord, who for our sake endured temptation and suffering.",
  it: "Venite, adoriamo Cristo Signore, che per noi volle essere tentato e soffrire.",
  es: "Venid, adoremos a Cristo el Señor, que por nosotros quiso ser tentado y padecer."
}
easter: {
  en: "The Lord is risen, alleluia; come, let us worship him, alleluia.",
  it: "Il Signore è risorto, alleluia: venite, adoriamo, alleluia.",
  es: "El Señor ha resucitado, aleluya; venid, adorémosle, aleluya."
}

Apply to WHERE hour='lauds' AND invitatory IS NULL, joining liturgical_day on date.
```

---

### Step 4 — Fill `hours_prayer.collect`

Tell Claude:
```
Copy collect values from liturgy_proper into hours_prayer for lauds and vespers:

UPDATE hours_prayer SET collect = (
    SELECT lp.collect FROM liturgy_proper lp
    WHERE lp.date = hours_prayer.date AND lp.lang = hours_prayer.lang
    AND lp.office = hours_prayer.hour
)
WHERE hour IN ('lauds', 'vespers') AND collect IS NULL;

Then for terce, copy from lauds of the same date:

UPDATE hours_prayer SET collect = (
    SELECT hp2.collect FROM hours_prayer hp2
    WHERE hp2.date = hours_prayer.date AND hp2.lang = hours_prayer.lang
    AND hp2.hour = 'lauds'
)
WHERE hour = 'terce' AND collect IS NULL;
```

---

### Step 5 — Fill `hours_prayer.responsory` (via Gemini)

The responsory varies by season. Send these prompts to Gemini one at a time and paste the JSON responses back to Claude for import.

**Prompt for Ordinary Time responsory:**
```
Generate the responsory texts for Ordinary Time in the Liturgy of the Hours (LHOD),
for Lauds, Terce, and Vespers, following the 4-week psalter cycle.

For each combination of psalter_week (1–4), day_of_week (1=Mon … 7=Sun),
and hour (lauds, terce, vespers), provide the short responsory in EN, IT, ES.

Format as a JSON array:
[{"psalter_week": 1, "day_of_week": 1, "hour": "lauds",
  "en": "...", "it": "...", "es": "..."}, ...]

Base these on the official Roman Rite LHOD (Liturgia Horarum).
Total: 4 weeks × 7 days × 3 hours = 84 objects.
```

**Prompt for Advent responsory:**
```
Same request as above but for the Advent season.
Advent has 4 weeks. Use psalter_week 1–4, day_of_week 1–7, hours lauds/terce/vespers.
Note: Advent week 4 may be short (ends Dec 24) — include all days up to and including day 4.
Format: same JSON array as above. Total: up to 84 objects.
```

**Prompt for Christmas responsory:**
```
Same request but for the Christmas season.
Christmas uses week_number 0–3 (week 0 = days before Jan 1,
weeks 1–3 = post-Epiphany). Use week 0–3, day_of_week 1–7, hours lauds/terce/vespers.
Format: same JSON array. Total: up to 84 objects.
```

**Prompt for Lent responsory:**
```
Same request but for Lent.
Lent has weeks 0–6 (week 0 = Ash Wednesday week).
Use week_number 0–6, day_of_week 1–7 (not all days exist in week 0 — include all that do),
hours lauds/terce/vespers.
Format: same JSON array.
```

**Prompt for Easter responsory:**
```
Same request but for Easter (Eastertide).
Easter has 8 weeks. All three hours (lauds, terce, vespers) use alleluia-based responsories.
Use week_number 1–8, day_of_week 1–7, hours lauds/terce/vespers.
Format: same JSON array.
```

After pasting each response, tell Claude:
```
Import this responsory JSON into hours_prayer.responsory.
Match on: ld.season = '[season]', psalter_week = week_number % 4 (if 0 use 4),
day_of_week, and hour. Only update rows where responsory IS NULL.
```

---

### Step 6 — Fill `hours_prayer.benedictus_magnificat` and `liturgy_proper.benedictus_ant` / `magnificat_ant` (via Gemini)

**Step 6a — Ordinary Time (psalter cycle, 28 unique texts)**

Send to Gemini:
```
Generate the Benedictus antiphon (for Lauds) and Magnificat antiphon (for Vespers)
for Ordinary Time in the Roman Rite LHOD, following the 4-week psalter cycle.

For each combination of psalter_week (1–4) and day_of_week (1=Mon … 7=Sun),
provide both antiphons in EN, IT, ES.

Format as JSON array:
[{"psalter_week": 1, "day_of_week": 1,
  "benedictus": {"en": "...", "it": "...", "es": "..."},
  "magnificat": {"en": "...", "it": "...", "es": "..."}}, ...]

Total: 28 objects.
```

Tell Claude to import, then apply a "psalter fallback" to all remaining NULL rows in other seasons:
```
After importing ordinary time antiphons, apply a psalter fallback to all remaining
NULL benedictus_magnificat rows in hours_prayer (all seasons), using the same
ordinary time 4-week cycle:
  psalter_week = week_number % 4, if 0 use 4
Match day_of_week. Apply benedictus text to hour='lauds', magnificat to hour='vespers'.
Also update liturgy_proper.benedictus_ant (office='lauds') and magnificat_ant (office='vespers')
with the same texts.
```

**Step 6b — Season-specific antiphons (override the fallback)**

Send one prompt per season to Gemini, then paste responses to Claude for import.

*Advent:*
```
Generate the Benedictus antiphon (Lauds) and Magnificat antiphon (Vespers) for
ferial days of Advent, Roman Rite LHOD. Weeks 1–4, days 1–7 (week 4 ends Dec 24).
Include the O Antiphons for Dec 17–23.
Format: [{"week": 1, "day": 1,
  "benedictus": {"en":"...","it":"...","es":"..."},
  "magnificat": {"en":"...","it":"...","es":"..."}}]
```

*Lent:*
```
Generate the Benedictus antiphon (Lauds) and Magnificat antiphon (Vespers) for
ferial days of Lent, Roman Rite LHOD. Weeks 0–6, days 1–7
(week 0 = Ash Wednesday week, week 6 = Holy Week).
Base antiphons on the daily Gospel reading for each day.
Same JSON format.
```

*Easter:*
```
Generate the Benedictus antiphon (Lauds) and Magnificat antiphon (Vespers) for
ferial days of Eastertide, Roman Rite LHOD. Weeks 1–8, days 1–7.
All antiphons should end with "alleluia".
Same JSON format.
```

*Christmas:*
```
Generate the Benedictus antiphon (Lauds) and Magnificat antiphon (Vespers) for
ferial days of the Christmas season, Roman Rite LHOD. Weeks 0–3, days 1–7
(week 0 = Christmas octave, weeks 1–3 = after Epiphany).
Same JSON format.
```

After pasting each response, tell Claude:
```
Import this [season] antiphon JSON. Override existing benedictus_magnificat in hours_prayer
and benedictus_ant/magnificat_ant in liturgy_proper for season='[season]'.
Match on week_number and day_of_week.
After import, fix any Spanish texts: replace 'alleluya' with 'aleluya'.
```

---

### Step 7 — Fill `hours_prayer.intercessions` (via Gemini)

Send this single prompt to Gemini:
```
Generate intercessions for Lauds and Vespers in the Roman Rite LHOD,
one set per season (ordinary, advent, christmas, lent, easter).
Each set = 5 petitions with a fixed response.
Format:
[{"season": "ordinary", "hour": "lauds",
  "en": ["Petition 1. ℟ Response.", "Petition 2. ℟ Response.", ...],
  "it": [...], "es": [...]}, ...]
Total: 5 seasons × 2 hours = 10 objects.
```

Tell Claude:
```
Import this intercessions JSON into hours_prayer.intercessions.
For each (season, hour, lang): join all 5 strings with '\n' and store as a single text value.
Apply to all rows WHERE hour IN ('lauds','vespers') AND intercessions IS NULL,
joining liturgical_day on date to get the season.
```

---

### Step 8 — Final validation

Tell Claude:
```
Run a final validation on data/prayers.db:

1. Check all applicable columns have 0 NULL in the right hours:
   - responsory: 0 NULL for lauds/terce/vespers
   - invitatory: 0 NULL for lauds
   - benedictus_magnificat: 0 NULL for lauds/vespers
   - intercessions: 0 NULL for lauds/vespers
   - collect: 0 NULL for lauds/terce/vespers

2. Check consistency: for every lauds/vespers row, hours_prayer.benedictus_magnificat
   must equal liturgy_proper.benedictus_ant (lauds) or magnificat_ant (vespers).

3. Check no Spanish texts contain 'alleluya' (should be 'aleluya').

4. Print a summary table of all checks with OK/FAIL status.
```

---

### Step 9 — Commit and push

Tell Claude:
```
Commit data/prayers.db with message:
"Generate YYYY DB: liturgical year YYYY-01-01 → YYYY-12-31"
Then push to main.
```

---

## Quick reference — column applicability by hour

| Column | lauds | terce | vespers | compline |
|--------|-------|-------|---------|----------|
| `invitatory` | ✓ | — | — | — |
| `hymn` | ✓ | ✓ | ✓ | ✓ |
| `antiphon_1/2` + `psalm_1/2` | ✓ | ✓ | ✓ | ✓ |
| `short_reading` | ✓ | ✓ | ✓ | ✓ |
| `responsory` | ✓ | ✓ | ✓ | — |
| `benedictus_magnificat` | ✓ (Benedictus) | — | ✓ (Magnificat) | — |
| `intercessions` | ✓ | — | ✓ | — |
| `collect` | ✓ | ✓ | ✓ | — |

Dashes = expected NULL, not a bug.
