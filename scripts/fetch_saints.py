#!/usr/bin/env python3
"""
Fetches daily saints from cpbjr.github.io
and enriches with Wikipedia biographies in 4 languages
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

API_URL = "https://cpbjr.github.io/catholic-readings-api/saints"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "saints"
WIKI_BASE = "https://{lang}.wikipedia.org/api/rest_v1/page/summary"

def ensure_raw_dir():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

def log_error(message: str):
    """Log error with timestamp"""
    log_file = Path(__file__).parent.parent / "data" / "raw" / "errors.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}: {message}\n")

def get_wikipedia_bio(saint_name: str, lang: str) -> str:
    """Fetch biography from Wikipedia in specified language"""
    try:
        url = WIKI_BASE.format(lang=lang)
        response = requests.get(f"{url}/{saint_name}", timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('extract', '')
    except:
        return None

def fetch_saint_day(date_str: str) -> dict:
    """
    Fetch saint info for a specific date.
    
    Args:
        date_str: Date in format "YYYY-MM-DD"
    
    Returns:
        Dict with date, name_it, name_en, name_es, name_pt,
               type_it, type_en, type_es, type_pt,
               bio_it, bio_en, bio_es, bio_pt
    """
    ensure_raw_dir()
    
    # Check if already fetched (and has resolved biographies)
    raw_file = RAW_DIR / f"{date_str}.json"
    if raw_file.exists():
        with open(raw_file, 'r', encoding='utf-8') as f:
            cached = json.load(f)
        # Only use cache if it has resolved biographies (not just raw API response)
        if 'bio_it' in cached:
            print(f"  {date_str}: Already fetched, skipping...")
            return cached
    
    # Parse date
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        mm_dd = f"{dt.month:02d}-{dt.day:02d}"
    except ValueError:
        log_error(f"Invalid date format: {date_str}")
        return None
    
    # Fetch from API
    url = f"{API_URL}/2026/{mm_dd}.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
    except requests.exceptions.RequestException as e:
        log_error(f"Failed to fetch saint for {date_str}: {e}")
        return None
    
    # Extract saint data
    saint_data = raw_data.get('saint', {})
    saint_name = saint_data.get('name', '')
    saint_type = saint_data.get('type', 'Memorial')
    
    result = {
        'date': date_str,
    }
    
    # Get biographies in all languages
    for lang_code, wiki_lang in [('it', 'it'), ('en', 'en'), ('es', 'es'), ('pt', 'pt')]:
        print(f"    Fetching {saint_name} bio in {wiki_lang.upper()}...")
        
        bio = get_wikipedia_bio(saint_name, wiki_lang)
        
        # Fallback to English if not found
        if not bio and wiki_lang != 'en':
            bio = get_wikipedia_bio(saint_name, 'en')
        
        result[f'name_{lang_code}'] = saint_name
        result[f'type_{lang_code}'] = saint_type
        result[f'bio_{lang_code}'] = bio or ''
    
    # Save completed result to file (with biographies resolved)
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result

def main(start_date: str = "2026-01-01", end_date: str = "2026-12-31"):
    """Fetch saint info for entire date range"""
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
        
        # Progress indicator
        if count % 10 == 0:
            print(f"  Progress: {count} saints fetched ({current.strftime('%Y-%m-%d')})")
        
        current += timedelta(days=1)
    
    print(f"Complete: {count} saints fetched")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test-date':
        if len(sys.argv) > 2:
            test_date = sys.argv[2]
            print(f"Testing with date: {test_date}")
            result = fetch_saint_day(test_date)
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("Failed to fetch saint")
        else:
            print("Usage: fetch_saints.py --test-date YYYY-MM-DD")
    else:
        main()
