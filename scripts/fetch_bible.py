#!/usr/bin/env python3
"""
Fetches biblical passages from api.scripture.api.bible
Resolves references like "Matthew 1:16,18-21,24" to full text
"""
import os
import re
import time
import requests
from typing import Optional, Dict

API_BASE = "https://rest.api.bible/v1"

# Bible IDs per language
BIBLE_IDS = {
    'it': None,  # Will be fetched dynamically
    'en': 'de4e12af7f28f599-02',  # King James Version
    'es': None,  # Will be fetched dynamically
    'pt': None,  # Will be fetched dynamically
}

def get_bible_id_for_language(lang: str, api_key: str) -> Optional[str]:
    """
    Fetch the first available Bible ID for a given language.
    """
    if BIBLE_IDS[lang]:
        return BIBLE_IDS[lang]
    
    lang_map = {'it': 'ita', 'es': 'spa', 'pt': 'por'}
    iso_lang = lang_map.get(lang, lang)
    
    headers = {'api-key': api_key}
    params = {'language': iso_lang}
    
    try:
        response = requests.get(f"{API_BASE}/bibles", headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('data') and len(data['data']) > 0:
            BIBLE_IDS[lang] = data['data'][0]['id']
            return BIBLE_IDS[lang]
    except Exception as e:
        print(f"ERROR: Could not fetch Bible ID for {lang}: {e}")
    
    return None

def normalize_reference(reference: str, lang: str) -> str:
    """
    Convert human-readable reference (e.g., "Matthew 1:16,18-21,24")
    to API format (e.g., "MAT.1.16,MAT.1.18-MAT.1.21,MAT.1.24")
    """
    book_map = {
        # Gospel
        'matthew': 'MAT', 'mark': 'MRK', 'luke': 'LUK', 'john': 'JHN',
        # Acts
        'acts': 'ACT',
        # Paul
        'romans': 'ROM', 'corinthians': 'CO1', '1 corinthians': 'CO1', '2 corinthians': 'CO2',
        'galatians': 'GAL', 'ephesians': 'EPH', 'philippians': 'PHP', 'colossians': 'COL',
        'thessalonians': 'TH1', '1 thessalonians': 'TH1', '2 thessalonians': 'TH2',
        'timothy': 'TI1', '1 timothy': 'TI1', '2 timothy': 'TI2',
        'titus': 'TIT', 'philemon': 'PHM',
        # Hebrews, James, Peter
        'hebrews': 'HEB', 'james': 'JAS',
        'peter': 'PE1', '1 peter': 'PE1', '2 peter': 'PE2',
        # John epistles
        'john': 'JHN',
        '1 john': 'JO1', '2 john': 'JO2', '3 john': 'JO3',
        # Jude, Revelation
        'jude': 'JUD', 'revelation': 'REV',
        # Old Testament
        'genesis': 'GEN', 'exodus': 'EXO', 'leviticus': 'LEV', 'numbers': 'NUM', 'deuteronomy': 'DEU',
        'joshua': 'JOS', 'judges': 'JDG', 'ruth': 'RUT',
        'samuel': 'SA1', '1 samuel': 'SA1', '2 samuel': 'SA2',
        'kings': 'KI1', '1 kings': 'KI1', '2 kings': 'KI2',
        'chronicles': 'CH1', '1 chronicles': 'CH1', '2 chronicles': 'CH2',
        'ezra': 'EZR', 'nehemiah': 'NEH', 'esther': 'EST',
        'job': 'JOB', 'psalm': 'PSA', 'psalms': 'PSA', 'proverbs': 'PRO',
        'ecclesiastes': 'ECC', 'song': 'SNG', 'song of songs': 'SNG', 'isaiah': 'ISA',
        'jeremiah': 'JER', 'lamentations': 'LAM', 'ezekiel': 'EZK', 'daniel': 'DAN',
        'hosea': 'HOS', 'joel': 'JOL', 'amos': 'AMO', 'obadiah': 'OBA',
        'jonah': 'JON', 'micah': 'MIC', 'nahum': 'NAH', 'habakkuk': 'HAB',
        'zephaniah': 'ZEP', 'haggai': 'HAG', 'zechariah': 'ZEC', 'malachi': 'MAL',
    }
    
    # Normalize input: remove extra spaces, make lowercase
    ref = re.sub(r'\s+', ' ', reference.strip()).lower()
    
    # Find book name
    book_abbr = None
    for book_name, abbr in book_map.items():
        if ref.startswith(book_name):
            book_abbr = abbr
            # Remove book name from reference
            ref = ref[len(book_name):].strip()
            break
    
    if not book_abbr:
        return None
    
    # Parse chapter and verses: "1:16,18-21,24"
    result = []
    parts = ref.split(',')
    
    for part in parts:
        part = part.strip()
        if ':' in part:
            chapter, verses = part.split(':', 1)
            chapter = chapter.strip()
            
            if '-' in verses:
                # Range like "18-21"
                v_start, v_end = verses.split('-')
                result.append(f"{book_abbr}.{chapter}.{v_start.strip()}-{book_abbr}.{chapter}.{v_end.strip()}")
            else:
                # Single verse
                result.append(f"{book_abbr}.{chapter}.{verses.strip()}")
        else:
            # Chapter only, or might be continuation
            if part and part != '-':
                result.append(f"{book_abbr}.{part}")
    
    return ','.join(result) if result else None

def fetch_passage(reference: str, lang: str, api_key: str) -> Optional[str]:
    """
    Fetch a biblical passage in a given language.
    
    Args:
        reference: Human-readable reference like "Matthew 1:16,18-21,24"
        lang: Language code (it, en, es, pt)
        api_key: API key for api.scripture.api.bible
    
    Returns:
        Clean text of the passage, or None if not found
    """
    # Get Bible ID for language
    bible_id = get_bible_id_for_language(lang, api_key)
    if not bible_id:
        print(f"ERROR: Could not get Bible ID for language {lang}")
        return None
    
    # Normalize reference
    passage_id = normalize_reference(reference, lang)
    if not passage_id:
        print(f"ERROR: Could not normalize reference: {reference}")
        return None
    
    headers = {'api-key': api_key}
    params = {
        'content-type': 'text',
        'include-verse-numbers': 'false'
    }
    
    url = f"{API_BASE}/bibles/{bible_id}/passages/{passage_id}"
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                text = data.get('data', {}).get('content', '')
                # Clean up any remaining HTML/XML tags
                text = re.sub(r'<[^>]+>', '', text)
                text = text.strip()
                return text
            
            elif response.status_code == 404:
                print(f"WARNING: Passage not found: {reference} in {lang}")
                return None
            
            elif response.status_code == 429:
                # Rate limit
                print(f"WARN: Rate limit hit, waiting 60s...")
                time.sleep(60)
                retry_count += 1
                continue
            
            else:
                print(f"ERROR: HTTP {response.status_code} for {reference}: {response.text}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request failed for {reference} in {lang}: {e}")
            return None
    
    print(f"ERROR: Max retries exceeded for {reference} in {lang}")
    return None


if __name__ == '__main__':
    # Test
    import sys
    if len(sys.argv) > 2:
        ref = sys.argv[1]
        lang = sys.argv[2]
        api_key = os.environ.get('BIBLE_API_KEY')
        if not api_key:
            print("ERROR: BIBLE_API_KEY not set")
            sys.exit(1)
        
        text = fetch_passage(ref, lang, api_key)
        if text:
            print(f"\n{ref} ({lang.upper()}):\n{text}")
        else:
            print(f"Failed to fetch: {ref} ({lang})")
