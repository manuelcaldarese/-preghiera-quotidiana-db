#!/usr/bin/env python3
"""
Fetches daily saint/celebration data from calapi.inadiutorium.cz
and enriches with Wikipedia biographies in 4 languages.

Source: http://calapi.inadiutorium.cz/api/v0/{lang}/calendars/default/{Y}/{M}/{D}
Supported langs on calapi: it, en (es/pt fallback to en name)
"""
import os
import re
import sys
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

CALAPI_BASE = "http://calapi.inadiutorium.cz/api/v0/{lang}/calendars/default/{year}/{month}/{day}"
WIKI_BASE = "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{name}"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "saints"
MAPPING_FILE = Path(__file__).parent.parent / "data" / "saint_wikipedia_mapping.json"
HEADERS = {"User-Agent": "PreghieraQuotidiana/1.0 (liturgical-db-builder; educational)"}


def _load_mapping() -> dict:
    if MAPPING_FILE.exists():
        data = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
        return {k: v for k, v in data.items() if not k.startswith('_')}
    return {}

WIKI_MAPPING = _load_mapping()


def ensure_raw_dir():
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def log_error(message: str):
    log_file = Path(__file__).parent.parent / "data" / "raw" / "errors.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()}: {message}\n")


def fetch_calapi(year: int, month: int, day: int, lang: str = 'en') -> dict | None:
    url = CALAPI_BASE.format(lang=lang, year=year, month=month, day=day)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        log_error(f"calapi error {lang} {year}-{month:02d}-{day:02d}: {e}")
        return None


# Role descriptors that always appear after a comma — strip from here onward
_ROLE_PATTERN = re.compile(
    r',\s*(pope|bishop|bishops|priest|priests|monk|monks|deacon|deacons|'
    r'abbot|abbots|hermit|virgin|martyr|martyrs|confessor|religious|founder|'
    r'doctor|widow|emperor|king|queen|soldier|lay|missionary|evangelist'
    r')[^,]*$',
    re.IGNORECASE
)
# Strip "Husband of the Blessed Virgin Mary" and similar verbose appositives
_APPOSITIVE_PATTERN = re.compile(
    r'\s+(husband|wife|mother|father|son|daughter)\s+of\b.*$',
    re.IGNORECASE
)

# Non-person liturgical titles — skip Wikipedia lookup entirely
_SKIP_PATTERNS = [
    'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'octave', 'day of christmas', 'day of easter', 'week',
    'the most holy', 'the holy', 'immaculate heart', 'sacred heart',
    'our lord', 'our lady', 'the nativity', 'the epiphany', 'the baptism',
    'the presentation', 'the transfiguration', 'the assumption',
    'the exaltation', 'the dedication', 'corpus christi', 'pentecost',
    'ash wednesday', 'palm sunday', 'good friday', 'holy saturday',
    'easter', 'advent', 'christmas', 'lent', 'ordinary time',
    'all saints', 'all souls', 'solemnity', 'commemoration',
]


def is_person_saint(name: str) -> bool:
    """Return False for liturgical events/mysteries that aren't searchable people."""
    lower = name.lower()
    return not any(p in lower for p in _SKIP_PATTERNS)


def clean_saint_name(name: str) -> str:
    """Strip verbose role descriptors to get a searchable saint name."""
    cleaned = _ROLE_PATTERN.sub('', name).strip()
    cleaned = _APPOSITIVE_PATTERN.sub('', cleaned).strip()
    # Remove trailing parenthetical e.g. "Mary, Mother of God (Octave of Christmas)"
    cleaned = re.sub(r'\s*\(.*\)$', '', cleaned).strip()
    # "Saints X and Y" → "X and Y" for multi-saint search
    cleaned = re.sub(r'^Saints?\s+', '', cleaned, flags=re.IGNORECASE).strip()
    # If multi-saint "X and Y" or "X, monk, and Y", take first name only
    cleaned = re.split(r',\s*(?:monk|bishop|deacon|priest)\s*,|,\s*and\b|\band\b', cleaned)[0].strip()
    return cleaned


def _wiki_get(url: str) -> requests.Response | None:
    """GET with short timeout. On 429 or error, return None immediately (no retry)."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code == 429:
            print(f"      Wikipedia rate limit — skipping")
            return None
        return resp
    except Exception:
        return None


def _title_candidates(name: str) -> list[str]:
    """Generate Wikipedia title candidates for a cleaned saint name."""
    slug = name.replace(' ', '_')
    return [
        slug,                        # "Catherine_of_Siena", "Fabian"
        f"Saint_{slug}",             # "Saint_George", "Saint_Agnes"
        f"Pope_{slug}",              # "Pope_Fabian"
        f"{slug}_(saint)",           # "X_(saint)"
        f"{slug}_(martyr)",          # "X_(martyr)"
    ]


_NON_PERSON_DESCRIPTIONS = (
    'given name', 'surname', 'name list', 'masculine name', 'feminine name',
    'municipality', 'commune', 'village', 'town', 'city', 'parish',
    'island', 'river', 'mountain', 'lake', 'country', 'region',
    'ship', 'film', 'song', 'album', 'television',
)


def fetch_wiki_summary(title: str, lang: str) -> tuple[str, str]:
    """Fetch Wikipedia summary for an exact title slug (e.g. 'Vincent_of_Saragossa'). Returns (bio, url)."""
    url = WIKI_BASE.format(lang=lang, name=requests.utils.quote(title))
    resp = _wiki_get(url)
    if not resp or resp.status_code == 404 or not resp.ok:
        return '', ''
    data = resp.json()
    if data.get('type') == 'disambiguation':
        return '', ''
    description = data.get('description', '').lower()
    if any(skip in description for skip in _NON_PERSON_DESCRIPTIONS):
        return '', ''
    return data.get('extract', ''), data.get('content_urls', {}).get('desktop', {}).get('page', '')


def fetch_wiki_summary_by_name(name: str, lang: str) -> tuple[str, str]:
    """Try multiple title candidates via REST summary API. Returns (bio, url)."""
    for title in _title_candidates(name):
        url = WIKI_BASE.format(lang=lang, name=title)
        resp = _wiki_get(url)
        if resp and resp.status_code == 200:
            data = resp.json()
            if data.get('type') in ('disambiguation', 'Internal error'):
                continue
            description = data.get('description', '').lower()
            if any(skip in description for skip in _NON_PERSON_DESCRIPTIONS):
                continue
            bio = data.get('extract', '')
            wiki_url = data.get('content_urls', {}).get('desktop', {}).get('page', '')
            if bio:
                return bio, wiki_url
        time.sleep(0.4)
    return '', ''


def get_wikipedia_bio(saint_name: str, lang: str, en_bio: str = '', en_url: str = '') -> tuple[str, str]:
    """Returns (bio_text, wikipedia_url) or ('', '').
    Uses only REST API (no w/api.php) to avoid rate limits.
    For non-EN: tries same title candidates in target lang, falls back to EN bio.
    """
    if not saint_name:
        return '', ''

    bio, url = fetch_wiki_summary_by_name(saint_name, lang)
    if bio:
        return bio, url

    # Fallback to English bio if available
    if en_bio:
        return en_bio, en_url
    return '', ''


def fetch_saint_day(date_str: str) -> dict | None:
    """
    Fetch saint info for a specific date.
    Returns dict with date, name_{lang}, feast_type_{lang}, bio_{lang}, wikipedia_url_{lang}
    for langs: it, en, es, pt
    """
    ensure_raw_dir()

    raw_file = RAW_DIR / f"{date_str}.json"
    if raw_file.exists():
        with open(raw_file, 'r', encoding='utf-8') as f:
            cached = json.load(f)
        if 'bio_it' in cached:
            print(f"  {date_str}: Already fetched, skipping...")
            return cached

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        log_error(f"Invalid date format: {date_str}")
        return None

    # Fetch from calapi (it and en are supported)
    data_en = fetch_calapi(dt.year, dt.month, dt.day, 'en')
    data_it = fetch_calapi(dt.year, dt.month, dt.day, 'it')

    celebrations_en = (data_en or {}).get('celebrations', [])
    celebrations_it = (data_it or {}).get('celebrations', [])

    # Pick the primary celebration (highest rank = lowest rank_num, or first)
    def primary(celebrations):
        if not celebrations:
            return None
        return min(celebrations, key=lambda c: c.get('rank_num', 99))

    cel_en = primary(celebrations_en)
    cel_it = primary(celebrations_it)

    name_en = (cel_en or {}).get('title', '')
    name_it = (cel_it or {}).get('title', name_en)
    feast_type_en = (cel_en or {}).get('rank', '')
    feast_type_it = (cel_it or {}).get('rank', feast_type_en)

    result = {
        'date': date_str,
        'name_it': name_it,
        'name_en': name_en,
        'name_es': name_en,   # calapi doesn't support es — use en name
        'name_pt': name_en,   # calapi doesn't support pt — use en name
        'feast_type_it': feast_type_it,
        'feast_type_en': feast_type_en,
        'feast_type_es': feast_type_en,
        'feast_type_pt': feast_type_en,
    }

    # Fetch Wikipedia bios only for actual person-saints (skip liturgical events)
    search_name = clean_saint_name(name_en)
    # Resolve Wikipedia title: mapping takes priority
    if name_en in WIKI_MAPPING:
        mapped_title = WIKI_MAPPING[name_en]
        if not mapped_title:
            # Explicitly mapped as empty → no Wikipedia bio
            print(f"    {date_str}: Skipping Wikipedia — mapped as empty for '{name_en}'")
            for lang in ['en', 'it', 'es', 'pt']:
                result[f'bio_{lang}'] = ''
                result[f'wikipedia_url_{lang}'] = ''
        else:
            print(f"    {date_str}: Wikipedia via mapping → '{mapped_title}'")
            bio_en, url_en = fetch_wiki_summary(mapped_title, 'en')
            result['bio_en'] = bio_en
            result['wikipedia_url_en'] = url_en
            time.sleep(0.4)
            # For other langs: try same slug directly, fallback to EN bio
            for lang in ['it', 'es', 'pt']:
                bio, wiki_url = fetch_wiki_summary(mapped_title, lang)
                time.sleep(0.4)
                if not bio:
                    bio, wiki_url = bio_en, url_en
                result[f'bio_{lang}'] = bio
                result[f'wikipedia_url_{lang}'] = wiki_url
    elif not is_person_saint(name_en):
        print(f"    {date_str}: Skipping Wikipedia — liturgical event '{name_en}'")
        for lang in ['en', 'it', 'es', 'pt']:
            result[f'bio_{lang}'] = ''
            result[f'wikipedia_url_{lang}'] = ''
    else:
        print(f"    {date_str}: Wikipedia bio [en] for '{search_name}'...")
        bio_en, url_en = get_wikipedia_bio(search_name, 'en')
        result['bio_en'] = bio_en
        result['wikipedia_url_en'] = url_en
        time.sleep(0.4)
        for lang in ['it', 'es', 'pt']:
            bio, wiki_url = get_wikipedia_bio(search_name, lang, en_bio=bio_en, en_url=url_en)
            result[f'bio_{lang}'] = bio
            result[f'wikipedia_url_{lang}'] = wiki_url
            time.sleep(0.4)

    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


def main(start_date: str = "2026-01-01", end_date: str = "2026-12-31"):
    print(f"Fetching saints from {start_date} to {end_date}...")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current = start
    count = 0

    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        try:
            result = fetch_saint_day(date_str)
            if result:
                count += 1
        except Exception as e:
            log_error(f"Unexpected error for {date_str}: {e}")

        if count % 10 == 0 and count > 0:
            print(f"  Progress: {count} saints fetched ({date_str})")

        current += timedelta(days=1)

    print(f"Complete: {count} saints fetched")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test-date':
        if len(sys.argv) > 2:
            result = fetch_saint_day(sys.argv[2])
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("Failed to fetch saint")
        else:
            print("Usage: fetch_saints.py --test-date YYYY-MM-DD")
    else:
        main()
