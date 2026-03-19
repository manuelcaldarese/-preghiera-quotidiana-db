#!/usr/bin/env python3
"""
Fetches daily gospel readings from cpbjr.github.io
and resolves the biblical references using fetch_bible.py
"""
import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from fetch_bible import fetch_passage

API_URL = "https://cpbjr.github.io/catholic-readings-api/readings"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "gospel"

def ensure_raw_dir():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

def log_error(message: str):
    """Log error with timestamp"""
    log_file = Path(__file__).parent.parent / "data" / "raw" / "errors.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}: {message}\n")

def fetch_gospel_day(date_str: str) -> dict:
    """
    Fetch gospel readings for a specific date.
    
    Args:
        date_str: Date in format "YYYY-MM-DD"
    
    Returns:
        Dict with keys: date, season, gospel_ref, gospel_text_it, gospel_text_en,
                        gospel_text_es, gospel_text_pt, reading_1_ref, reading_1_text_it,
                        reading_1_text_en, reading_1_text_es, reading_1_text_pt
    """
    ensure_raw_dir()
    
    # Check if already fetched (and has resolved texts)
    raw_file = RAW_DIR / f"{date_str}.json"
    if raw_file.exists():
        with open(raw_file, 'r', encoding='utf-8') as f:
            cached = json.load(f)
        # Only use cache if it has resolved gospel texts (not just raw API response)
        if 'gospel_text_it' in cached:
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
        log_error(f"Failed to fetch gospel for {date_str}: {e}")
        return None
    
    # Extract data
    api_key = os.environ.get('BIBLE_API_KEY')
    if not api_key:
        log_error(f"BIBLE_API_KEY not set")
        return None
    
    readings = raw_data.get('readings', {})
    gospel_ref = readings.get('gospel', '')
    reading_1_ref = readings.get('firstReading', '')
    
    # Resolve texts in all languages
    result = {
        'date': date_str,
        'season': raw_data.get('season', ''),
        'gospel_ref': gospel_ref,
        'reading_1_ref': reading_1_ref,
    }
    
    for lang in ['it', 'en', 'es', 'pt']:
        print(f"    Fetching gospel text in {lang.upper()}...")
        gospel_text = fetch_passage(gospel_ref, lang, api_key)
        result[f'gospel_text_{lang}'] = gospel_text or ''
        
        reading_1_text = fetch_passage(reading_1_ref, lang, api_key)
        result[f'reading_1_text_{lang}'] = reading_1_text or ''
        
        time.sleep(1)  # 1 second delay between calls
    
    # Save completed result to file (with resolved texts)
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result

def main(start_date: str = "2026-01-01", end_date: str = "2026-12-31"):
    """Fetch gospel readings for entire date range"""
    print(f"Fetching gospel readings from {start_date} to {end_date}...")
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    current = start
    count = 0
    
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        try:
            result = fetch_gospel_day(date_str)
            if result:
                count += 1
        except Exception as e:
            log_error(f"Unexpected error for {date_str}: {e}")
        
        # Progress indicator
        if count % 10 == 0:
            print(f"  Progress: {count} days fetched ({current.strftime('%Y-%m-%d')})")
        
        current += timedelta(days=1)
    
    print(f"Complete: {count} gospel readings fetched")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test-date':
        if len(sys.argv) > 2:
            test_date = sys.argv[2]
            print(f"Testing with date: {test_date}")
            result = fetch_gospel_day(test_date)
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("Failed to fetch gospel")
        else:
            print("Usage: fetch_gospel.py --test-date YYYY-MM-DD")
    else:
        main()
