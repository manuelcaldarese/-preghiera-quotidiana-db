# Preghiera Quotidiana Database

A Python system to build and populate a SQLite database (`data/prayers.db`) with multilingual Catholic liturgical content for the entire year 2026. Integrates data from multiple sources to create a comprehensive daily prayer resource.

## Overview

This project fetches and aggregates Catholic daily readings, saint information, prayer data, and Liturgy of the Hours content in 4 languages (Italian, English, Spanish, Portuguese) for every day of 2026.

## Database State (as of 2026-03-22)

### Schema — 11 tables

| Table | Rows | Description |
|-------|------|-------------|
| `gospel` | 1,460 | Daily Mass gospel + first reading + psalm — 365 days × 4 languages |
| `saint` | 1,460 | Daily saint info with Wikipedia biography — 365 days × 4 languages |
| `prayer` | 72 | 18 traditional Catholic prayers × 4 languages |
| `rosary_mystery` | 80 | 20 mysteries (Joyful, Sorrowful, Glorious, Luminous) × 4 languages |
| `via_crucis` | 56 | 14 Stations of the Cross × 4 languages |
| `novena` | 180 | 5 novenas × 9 days × 4 languages |
| `liturgical_day` | 365 | Liturgical calendar metadata for 2026 (season, color, rank, etc.) |
| `liturgy_proper` | 2,190 | Liturgy of the Hours core (Lauds + Vespers) — 365 days × 3 languages (IT, EN, ES) |
| `hours_prayer` | 2,190 | Liturgy of the Hours extended: adds hymn, invitatory, responsory — 365 days × 3 languages |
| `feast_calendar` | 188 | Saint name → feast day mapping with name variants in 4 languages |
| `saint_greeting` | 544 | Personalized feast-day greetings for saints, in 4 languages |

### Data Quality

- `gospel`: 0 empty texts, 0 missing names, full 2026 coverage
- `saint`: 0 missing names; 61/365 dates have Wikipedia biography (the rest are liturgical events without a dedicated saint)
- `liturgy_proper`: 100% date coverage; `antiphon_1` and `short_reading` always populated; `collect` NULL for 6 edge-case days
- `prayer`: 18 prayers — Lord's Prayer, Hail Mary, Glory Be, Apostles' Creed, Angelus, Regina Coeli, Memorare, Te Deum, Divine Mercy Chaplet, Prayer of Saint Francis, Morning Prayer, Evening Prayer, Examination of Conscience, Prayer Before Confession, Prayer After Communion, Prayer for the Dead, Prayer for the Sick, Act of Contrition

---

## Architecture

### Database Schema

```
gospel (date, lang, reference, title, text, reading_1_ref, reading_1_text, psalm_ref, psalm_text, source)
  - 365 days × 4 languages = 1,460 rows ✅

saint (date, lang, name, short_bio, ...)
  - 365 days × 4 languages = 1,460 rows ✅

prayer (key, lang, category, title, text)
  - 18 prayers × 4 languages = 72 rows ✅

rosary_mystery (type, number, lang, title, description, ...)
  - 20 mysteries × 4 languages = 80 rows ✅

via_crucis (...)
  - 14 stations × 4 languages = 56 rows ✅

novena (...)
  - 5 novenas × 9 days × 4 languages = 180 rows ✅

liturgical_day (date, season, week_number, day_of_week, celebration_name, celebration_type, liturgical_color, is_sunday, is_holy_day)
  - 365 rows ✅

liturgy_proper (date, lang, office, antiphon_1, antiphon_2, antiphon_3, short_reading, short_reading_ref, collect, benedictus_ant, magnificat_ant)
  - 365 days × 3 languages × 2 offices (lauds/vespers) = 2,190 rows ✅
  - Source: DivinumOfficium (github.com/DivinumOfficium/divinum-officium)
  - Languages: IT, EN, ES (PT not available in DivinumOfficium)

hours_prayer (date, lang, hour, invitatory, hymn, antiphon_1, psalm_1_ref, psalm_1_text, antiphon_2, psalm_2_ref, psalm_2_text, short_reading, short_reading_ref, responsory, benedictus_magnificat, intercessions, collect)
  - 365 days × 3 languages × 2 hours (lauds/vespers) = 2,190 rows ✅
  - Extends liturgy_proper with hymn text, invitatory antiphon, responsory
  - psalm_1/2_text and intercessions are NULL (app-side responsibility)

feast_calendar (month, day, saint_name, names_it, names_en, names_es, names_pt, feast_rank)
  - 188 rows ✅

saint_greeting (saint_name, lang, greeting_short, greeting_long, fun_fact)
  - 544 rows ✅
```

### External APIs & Sources

- **rest.api.bible**: `https://rest.api.bible/v1/` — Bible passages
  - Auth: `api-key` header
  - Handles rate limiting (429) with 60s retry

- **cpbjr.github.io**: Catholic daily readings and saints
  - `/readings/2026/{MM-DD}.json`
  - `/saints/2026/{MM-DD}.json`

- **Wikipedia REST API**: Saint biographies
  - `https://{lang}.wikipedia.org/api/rest_v1/page/summary/{name}`
  - Languages: it, en, es, pt (with en fallback)

- **calapi.inadiutorium.cz**: Liturgical calendar metadata
  - Used to populate `liturgical_day`

- **DivinumOfficium** (local clone): Liturgy of the Hours text
  - `github.com/DivinumOfficium/divinum-officium`
  - Cloned to `/workspaces/divinum-officium/`
  - Languages: Italiano, English, Espanol

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Install

```bash
# Clone or enter workspace
cd /workspaces/-preghiera-quotidiana-db

# Install dependencies
pip install -r scripts/requirements.txt

# Create .env file with API key
echo "BIBLE_API_KEY=<your_api_key_here>" > .env

# Clone DivinumOfficium (needed for liturgy_proper only)
git clone --depth=1 --filter=blob:none --sparse https://github.com/DivinumOfficium/divinum-officium.git /workspaces/divinum-officium
cd /workspaces/divinum-officium
git sparse-checkout set web/www/horas/Italiano web/www/horas/English web/www/horas/Espanol
git checkout
cd /workspaces/-preghiera-quotidiana-db
```

### Build Database

```bash
# Full build for 2026 (default)
python3 scripts/build_db.py

# Full build for a different year
python3 scripts/build_db.py --year 2027

# Populate Liturgy of the Hours only (requires DivinumOfficium clone above)
python3 scripts/populate_liturgy_proper.py
python3 scripts/populate_hours_prayer.py

# Validate the DB
python3 scripts/validate_db.py
```

---

## Scripts

| Script | Description |
|--------|-------------|
| `build_db.py` | Main orchestrator: creates schema, fetches all data, populates all tables |
| `fetch_gospel.py` | Fetches daily gospel readings in 4 languages with caching |
| `fetch_saints.py` | Fetches saint data + Wikipedia biographies in 4 languages |
| `fetch_bible.py` | Parses biblical references and fetches full verse text |
| `fetch_liturgical_day.py` | Fetches liturgical calendar metadata from calapi |
| `populate_prayers.py` | Populates the `prayer` table (included in build_db.py) |
| `populate_rosary.py` | Populates the `rosary_mystery` table (included in build_db.py) |
| `populate_via_crucis.py` | Populates the `via_crucis` table |
| `populate_novene.py` | Populates the `novena` table |
| `populate_feast_calendar.py` | Populates the `feast_calendar` table |
| `populate_saint_greeting.py` | Populates the `saint_greeting` table |
| `populate_liturgy_proper.py` | Populates `liturgy_proper` from DivinumOfficium source files |
| `populate_hours_prayer.py` | Populates `hours_prayer` — extends `liturgy_proper` with hymn, invitatory, responsory |
| `validate_db.py` | Validates row counts and data quality; exits 0 if production-ready |

---

## Languages Supported

| Language | gospel | saint | prayer | rosary | via_crucis | novena | liturgy_proper | hours_prayer |
|----------|--------|-------|--------|--------|------------|--------|----------------|--------------|
| 🇮🇹 Italian (it) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🇬🇧 English (en) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🇪🇸 Spanish (es) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🇵🇹 Portuguese (pt) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ (not in source) | ❌ (not in source) |

---

## API Keys & Environment

Create `.env` in workspace root:
```
BIBLE_API_KEY=your_api_key_here
```

Get a free API key: https://api.bible

---

## File Structure

```
/workspaces/-preghiera-quotidiana-db/
├── README.md
├── schema.sql                          # Database schema
├── data/
│   ├── prayers.db                      # Main SQLite database
│   ├── saint_wikipedia_mapping.json    # Saint → Wikipedia name mapping
│   └── raw/
│       ├── gospel/                     # Cached gospel JSON (365 files)
│       ├── saints/                     # Cached saint JSON (365 files)
│       ├── liturgical/                 # Cached liturgical day JSON (365 files)
│       └── errors.log                  # Error log from fetches
└── scripts/
    ├── build_db.py
    ├── fetch_bible.py
    ├── fetch_gospel.py
    ├── fetch_saints.py
    ├── fetch_liturgical_day.py
    ├── fetch_liturgy.py
    ├── populate_prayers.py
    ├── populate_rosary.py
    ├── populate_via_crucis.py
    ├── populate_novene.py
    ├── populate_feast_calendar.py
    ├── populate_saint_greeting.py
    ├── populate_liturgy_proper.py
    ├── populate_hours_prayer.py
    ├── validate_db.py
    ├── quick_test.py
    └── requirements.txt
```

---

## Note su `saint.short_bio`

61/365 date hanno bio Wikipedia. Le restanti sono eventi liturgici senza una pagina dedicata (es. "Feria del Tempo Ordinario") o santi non mappati nel catalogo Wikipedia.

Per rigenerare le bio mancanti dopo un rate limit Wikipedia:
```bash
# Verificare disponibilità:
curl -s -w "%{http_code}" -H "User-Agent: PreghieraQuotidiana/1.0" \
  "https://en.wikipedia.org/api/rest_v1/page/summary/Nereus_and_Achilleus" | tail -1
# Se 200:
rm data/raw/saints/2026-05-12.json
python3 scripts/fetch_saints.py --test-date 2026-05-12
python3 scripts/build_db.py
```

Il mapping completo è in `data/saint_wikipedia_mapping.json`.

---

## Note su `liturgy_proper`

I testi dell'Ufficio delle Ore provengono da **DivinumOfficium** (forma straordinaria del Rito Romano). Il database usa la forma ordinaria per il calendario (`liturgical_day`), quindi esiste una leggera divergenza nelle settimane del Tempo Ordinario — i testi rimangono appropriati alla stagione liturgica.

Fallback chain per ogni sezione:
1. File proprio della festa (`Sancti/MM-DD.txt`)
2. File stagionale (`Tempora/`)
3. Domenica della stessa settimana (per feriali senza Oratio/Capitulum)
4. Psalterium settimanale (per antifone feriali)
5. Lettura breve stagionale da `Psalterium/Special/Matutinum Special.txt`
