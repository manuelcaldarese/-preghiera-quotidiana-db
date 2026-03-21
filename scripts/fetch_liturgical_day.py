#!/usr/bin/env python3
"""
Fetches liturgical day metadata from calapi.inadiutorium.cz for each date in 2026
and populates the liturgical_day table.
"""
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

CALAPI_BASE = "http://calapi.inadiutorium.cz/api/v0/en/calendars/default/{year}/{month}/{day}"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "liturgical"
HEADERS = {"User-Agent": "PreghieraQuotidiana/1.0 (liturgical-db-builder; educational)"}

COLOUR_MAP = {
    'green': 'green', 'white': 'white', 'red': 'red',
    'violet': 'violet', 'purple': 'violet', 'rose': 'rose',
    'black': 'black', 'gold': 'white',
}


def ensure_raw_dir():
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_day(date_str: str) -> dict | None:
    ensure_raw_dir()
    raw_file = RAW_DIR / f"{date_str}.json"
    if raw_file.exists():
        return json.loads(raw_file.read_text(encoding='utf-8'))

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    url = CALAPI_BASE.format(year=dt.year, month=dt.month, day=dt.day)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  ERROR {date_str}: {e}")
        return None

    raw_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data


def parse_day(date_str: str, data: dict) -> dict:
    celebrations = data.get('celebrations', [])
    primary = min(celebrations, key=lambda c: c.get('rank_num', 99)) if celebrations else {}

    season = data.get('season', '')
    season_week = data.get('season_week', None)
    weekday = data.get('weekday', '')
    colour = COLOUR_MAP.get((primary.get('colour') or '').lower(), primary.get('colour', ''))
    celebration_name = primary.get('title', '')
    celebration_type = primary.get('rank', '')
    rank_num = primary.get('rank_num', 99)

    is_sunday = 1 if weekday == 'sunday' else 0
    is_holy_day = 1 if rank_num <= 1.3 else 0
    day_of_week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'].index(weekday) + 1 if weekday in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'] else 0

    return {
        'date': date_str,
        'season': season,
        'week_number': season_week,
        'day_of_week': day_of_week,
        'celebration_name': celebration_name,
        'celebration_type': celebration_type,
        'liturgical_color': colour,
        'is_sunday': is_sunday,
        'is_holy_day': is_holy_day,
    }


def get_all_rows(start: str = "2026-01-01", end: str = "2026-12-31") -> list[dict]:
    rows = []
    current = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    count = 0

    while current <= end_dt:
        date_str = current.strftime("%Y-%m-%d")
        data = fetch_day(date_str)
        if data:
            rows.append(parse_day(date_str, data))
            count += 1
            if count % 50 == 0:
                print(f"  {count} giorni processati...")
        time.sleep(0.1)
        current += timedelta(days=1)

    return rows


if __name__ == '__main__':
    rows = get_all_rows()
    print(f"Totale: {len(rows)} righe")
