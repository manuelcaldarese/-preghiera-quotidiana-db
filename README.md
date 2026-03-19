# Preghiera Quotidiana Database

A Python system to build and populate a SQLite database (`data/prayers.db`) with multilingual biblical content for the entire year 2026. Integrates data from multiple REST APIs to create a comprehensive liturgical resource.

## Overview

This project fetches and aggregates Catholic daily readings, saint information, and prayer data in 4 languages (Italian, English, Spanish, Portuguese) for every day of 2026.

## Current State of the Art

### ✅ Completed Features

**Core Infrastructure:**
- ✅ SQLite database schema with 6 tables (gospel, saint, prayer, rosary_mystery, liturgy_proper, liturgical_day)
- ✅ Environment-based API key management (via `.env` file)
- ✅ Database creation and schema initialization
- ✅ Indexed queries for fast lookups by date and language

**Data Population:**
- ✅ **Prayer Table**: 17 traditional Catholic prayers (Lord's Prayer, Hail Mary, Glory Be, etc.) in 4 languages (28 rows total)
- ✅ **Rosary Mysteries Table**: 20 mysteries (5 Joyful, 5 Sorrowful, 5 Glorious, 5 Luminous) with descriptions and scripture references in 4 languages (80 rows total)

**Data Fetching Modules:**
- ✅ `fetch_bible.py`: Parses human-readable biblical references (e.g., "Matthew 1:16,18-21") and fetches full verse text from rest.api.bible with language-specific Bible ID lookup
- ✅ `fetch_gospel.py`: Fetches daily gospel readings from cpbjr.github.io, resolves biblical text in 4 languages, implements intelligent caching with resolved data validation
- ✅ `fetch_saints.py`: Fetches saint information from cpbjr.github.io and enriches with Wikipedia biographies in 4 languages (with fallback to English if translation unavailable)
- ✅ API rate limiting and error handling with retry logic (429 status → 60s wait)
- ✅ Comprehensive error logging to `data/raw/errors.log`

**Recent Bug Fixes:**
- ✅ Fixed `fetch_gospel.py` cache bug: Now saves complete JSON with resolved `gospel_text_{lang}` fields AFTER fetching all language versions (not before)
- ✅ Fixed `fetch_saints.py` to save complete JSON with resolved `bio_{lang}` fields
- ✅ Added `.env` loading to `build_db.py` via `python-dotenv`
- ✅ Enhanced cache validation: Only uses cached files if they contain fully resolved data

### 🔄 In Progress

**Database Population:**
- Currently executing: Full year 2026 gospel and saint data fetching
- Expected: ~1,460 gospel rows (365 days × 4 languages)
- Expected: ~1,460 saint rows (365 days × 4 languages)
- Status: Gospel/saint fetching active, insertion pending

### ❌ Known Issues

1. **Column Name Mismatch** (needs fix):
   - `build_db.py` insert statement references non-existent columns:
     - `gospel_text` should be `text`
     - `biography` should be `short_bio`
     - `audio_tts_hint` doesn't exist on gospel/saint tables (only on prayer)

2. **Incomplete Data Population**:
   - gospel and saint tables still empty (0 rows) - waiting for fetches to complete and correct insert statements
   - liturgy_proper table not yet implemented
   - liturgical_day table not yet implemented

## Architecture

### Database Schema

```
gospel (date, lang, season, text, reading_1_text, ...)
  - 365 days × 4 languages = 1,460 rows (when complete)
  
saint (date, lang, name, short_bio, ...)
  - 365 days × 4 languages = 1,460 rows (when complete)
  
prayer (key, lang, category, title, text)
  - 17 prayers × 4 languages = 68 rows ✅ (complete)
  
rosary_mystery (type, number, lang, title, description, ...)
  - 20 mysteries × 4 languages = 80 rows ✅ (complete)
```

### External APIs

- **rest.api.bible**: `https://rest.api.bible/v1/` (Bible passages)
  - Auth: `api-key` header
  - Handles rate limiting (429) with retry
  
- **cpbjr.github.io**: Catholic daily readings and saints
  - Endpoint: `/readings/2026/{MM-DD}.json`
  - Endpoint: `/saints/2026/{MM-DD}.json`
  
- **Wikipedia REST API**: Saint biographies
  - `https://{lang}.wikipedia.org/api/rest_v1/page/summary/{name}`
  - Languages: it, en, es, pt (with en fallback)

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
```

### Build Database

```bash
# Full build (creates DB + fetches all 2026 data + populates tables)
python3 scripts/build_db.py

# Estimated time: ~1 hour
```

## Next Steps & Recommendations

### 🚨 Critical Fixes (Before Testing)

1. **Fix INSERT Statement Column Names**
   ```python
   # In build_db.py, fix these:
   # gospel: gospel_text → text, remove audio_tts_hint
   # saint: biography → short_bio, remove audio_tts_hint
   ```

2. **Verify Data Fetching Completes**
   - Monitor: `ls data/raw/gospel/ data/raw/saints/ | wc -l`
   - Expected: 365 JSON files in each directory

3. **Verify Data Insertion**
   - After build completes: `sqlite3 data/prayers.db "SELECT COUNT(*) FROM gospel;"`
   - Expected: 1460 rows

### 📝 Suggested Tests

#### Unit Tests (`tests/test_fetch_modules.py`)
```python
def test_fetch_gospel_day_returns_resolved_texts():
    """Verify gospel_text_it, gospel_text_en, etc. are present"""
    
def test_fetch_saint_day_returns_resolved_bios():
    """Verify bio_it, bio_en, etc. are present"""
    
def test_fetch_bible_normalizes_references():
    """Test: 'Matthew 1:16,18-21' → valid API format"""
    
def test_api_rate_limiting_honored():
    """Verify 1s delays between calls in fetch_gospel"""
```

#### Integration Tests (`tests/test_database_build.py`)
```python
def test_database_creation_succeeds():
    """Verify prayers.db created from schema.sql"""
    
def test_prayer_table_populated():
    """Verify 28 rows (17 prayers × 4 langs)"""
    
def test_rosary_mystery_table_populated():
    """Verify 80 rows (20 mysteries × 4 langs)"""
    
def test_gospel_table_multilingual():
    """For 2026-01-01: verify 4 rows (one per lang)"""
    
def test_saint_table_has_biographies():
    """Verify short_bio field populated for each date/lang"""
    
def test_resolved_gospel_text_not_references():
    """Verify gospel.text contains actual verses, not 'Matthew 1:16'"""
    
def test_cache_validation_skips_incomplete_data():
    """Verify cache files with missing gospel_text_* are re-fetched"""
```

#### Query Tests (`tests/test_queries.py`)
```python
def test_query_gospel_by_date_and_language():
    """SELECT * FROM gospel WHERE date='2026-01-01' AND lang='it'"""
    
def test_query_saint_by_date():
    """SELECT DISTINCT name FROM saint WHERE date='2026-03-19'"""
    
def test_query_prayer_by_category():
    """SELECT * FROM prayer WHERE category='rosary'"""
    
def test_multilingual_consistency():
    """Verify each date has 4 gospel rows (one per lang)"""
```

#### Data Validation Tests (`tests/test_data_quality.py`)
```python
def test_no_empty_gospel_texts():
    """gospel.text should never be empty string"""
    
def test_saint_names_not_null():
    """saint.name should always be populated"""
    
def test_dates_are_valid_iso8601():
    """All dates match YYYY-MM-DD format"""
    
def test_language_codes_valid():
    """lang column only contains: it, en, es, pt"""
```

### 📊 Performance & Quality

- Add query performance benchmarks (index usage)
- Validate all 1,460 gospel entries have non-empty text
- Check saint biography retrieval success rate (measure Wikipedia availability)
- Profile: Memory usage for full 365-day fetch

### 📚 Documentation Enhancements

- Add data dictionary (column meanings)
- Document API fallback behavior
- Create troubleshooting guide for API errors
- Add example queries for common use cases

### 🔮 Future Features

- Populate `liturgy_proper` table (Office antiphons, readings)
- Implement `liturgical_day` table with liturgical colors/week numbers
- Add caching strategy for Wikipedia (reduce redundant calls)
- Support historical years (not just 2026)
- Add TTS audio generation hints to saint biographies
- Create REST API layer on top of database
- Build web UI for daily prayer browsing

## File Structure

```
/workspace/
├── README.md (this file)
├── schema.sql                    # Database schema
├── data/
│   ├── prayers.db              # Main SQLite database
│   ├── raw/
│   │   ├── gospel/             # Cached gospel JSON (2026-01-01.json, ...)
│   │   ├── saints/             # Cached saint JSON (2026-01-01.json, ...)
│   │   └── errors.log          # Error log from fetches
│   ├── processed/
│   └── (future: processed data artifacts)
└── scripts/
    ├── build_db.py             # Main orchestrator
    ├── fetch_bible.py          # Bible passage fetching
    ├── fetch_gospel.py         # Gospel reading fetching
    ├── fetch_saints.py         # Saint data fetching
    ├── populate_prayers.py     # (included in build_db.py)
    ├── populate_rosary.py      # (included in build_db.py)
    └── requirements.txt
```

## API Keys & Environment

Create `.env` in workspace root:
```
BIBLE_API_KEY=your_api_key_here
```

Get a free API key: https://api.bible

## Languages Supported

- 🇮🇹 Italian (it)
- 🇬🇧 English (en)
- 🇪🇸 Spanish (es)
- 🇵🇹 Portuguese (pt)