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
        # Gospel — longer names before shorter to avoid prefix conflicts
        'matthew': 'MAT', 'mark': 'MRK', 'luke': 'LUK',
        # John epistles before John gospel to match "1 john" etc. first
        '1 john': 'JO1', '2 john': 'JO2', '3 john': 'JO3',
        'john': 'JHN',
        # Acts
        'acts': 'ACT',
        # Paul — numbered before generic
        '1 corinthians': 'CO1', '2 corinthians': 'CO2', 'corinthians': 'CO1',
        'galatians': 'GAL', 'ephesians': 'EPH', 'philippians': 'PHP', 'colossians': 'COL',
        '1 thessalonians': 'TH1', '2 thessalonians': 'TH2', 'thessalonians': 'TH1',
        '1 timothy': 'TI1', '2 timothy': 'TI2', 'timothy': 'TI1',
        'titus': 'TIT', 'philemon': 'PHM',
        'romans': 'ROM',
        # Hebrews, James, Peter
        'hebrews': 'HEB', 'james': 'JAS',
        '1 peter': 'PE1', '2 peter': 'PE2', 'peter': 'PE1',
        # Jude, Revelation
        'jude': 'JUD', 'revelation': 'REV',
        # Old Testament
        'genesis': 'GEN', 'exodus': 'EXO', 'leviticus': 'LEV', 'numbers': 'NUM', 'deuteronomy': 'DEU',
        'joshua': 'JOS', 'judges': 'JDG', 'ruth': 'RUT',
        '1 samuel': 'SA1', '2 samuel': 'SA2', 'samuel': 'SA1',
        '1 kings': 'KI1', '2 kings': 'KI2', 'kings': 'KI1',
        '1 chronicles': 'CH1', '2 chronicles': 'CH2', 'chronicles': 'CH1',
        'ezra': 'EZR', 'nehemiah': 'NEH', 'esther': 'EST',
        'job': 'JOB', 'psalm': 'PSA', 'psalms': 'PSA', 'proverbs': 'PRO',
        'ecclesiastes': 'ECC', 'song of songs': 'SNG', 'song': 'SNG', 'isaiah': 'ISA',
        'jeremiah': 'JER', 'lamentations': 'LAM', 'ezekiel': 'EZK', 'daniel': 'DAN',
        'hosea': 'HOS', 'joel': 'JOL', 'amos': 'AMO', 'obadiah': 'OBA',
        'jonah': 'JON', 'micah': 'MIC', 'nahum': 'NAH', 'habakkuk': 'HAB',
        'zephaniah': 'ZEP', 'haggai': 'HAG', 'zechariah': 'ZEC', 'malachi': 'MAL',
        # Deuterocanonical
        'sirach': 'SIR', 'ecclesiasticus': 'SIR',
        'wisdom': 'WIS', 'tobit': 'TOB', 'judith': 'JDT', 'baruch': 'BAR',
        '1 maccabees': 'MA1', '2 maccabees': 'MA2', 'maccabees': 'MA1',
    }

    # Normalize input: remove extra spaces, make lowercase
    ref = re.sub(r'\s+', ' ', reference.strip()).lower()

    # Handle "X or Y" alternatives: take only the first option
    ref = re.sub(r'\s+or\s+.*', '', ref)

    # Normalize em-dash and en-dash to regular hyphen
    ref = ref.replace('\u2014', '-').replace('\u2013', '-')

    # Normalize semicolons to commas (semicolons separate segments with their own chapter:verse)
    ref = ref.replace(';', ',')

    # Find book name (try longest match first to avoid prefix conflicts)
    book_abbr = None
    sorted_books = sorted(book_map.keys(), key=len, reverse=True)
    for book_name in sorted_books:
        if ref.startswith(book_name):
            book_abbr = book_map[book_name]
            ref = ref[len(book_name):].strip()
            break

    if not book_abbr:
        return None

    # Reject non-standard chapter formats (e.g. "Esther C:12" — Greek additions)
    # by checking that the first chapter token is numeric
    first_colon = ref.find(':')
    if first_colon != -1:
        chapter_token = ref[:first_colon].strip().lstrip(',').strip()
        if chapter_token and not chapter_token.isdigit():
            return None

    # Parse chapter and verses: "1:16,18-21,24a"
    result = []
    parts = ref.split(',')
    current_chapter = None

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Determine if this part starts with a chapter number (e.g. "18:9-10")
        # vs. being a pure verse continuation (e.g. "14b", "24-25a", "30-19:3").
        # A chapter-prefixed segment has a numeric token before the first colon.
        has_chapter_prefix = False
        if ':' in part:
            pre_colon = part.split(':', 1)[0].strip()
            # pre_colon is a chapter number only if it's a plain integer
            if pre_colon.isdigit():
                has_chapter_prefix = True

        if has_chapter_prefix:
            chapter, verses = part.split(':', 1)
            current_chapter = chapter.strip()
            verses = verses.strip()
        else:
            # Continuation segment: use current_chapter
            verses = part

        if not verses or not current_chapter:
            continue

        if not current_chapter.isdigit():
            continue

        if '-' in verses:
            v_start, v_end = verses.split('-', 1)
            v_start = re.sub(r'[a-z]+$', '', v_start.strip())

            # Cross-chapter range: v_end contains chapter:verse (e.g. "19:3")
            if ':' in v_end:
                end_chap, end_verse = v_end.split(':', 1)
                end_chap = end_chap.strip()
                end_verse = re.sub(r'[a-z]+$', '', end_verse.strip())
                result.append(
                    f"{book_abbr}.{current_chapter}.{v_start}-{book_abbr}.{end_chap}.{end_verse}"
                )
                current_chapter = end_chap
            else:
                v_end = re.sub(r'[a-z]+$', '', v_end.strip())
                result.append(
                    f"{book_abbr}.{current_chapter}.{v_start}-{book_abbr}.{current_chapter}.{v_end}"
                )
        else:
            v = re.sub(r'[a-z]+$', '', verses.strip())
            result.append(f"{book_abbr}.{current_chapter}.{v}")

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

    # The API /passages endpoint does not accept comma-separated multi-segment IDs.
    # Fetch each segment individually and concatenate.
    segments = passage_id.split(',')
    texts = []
    for segment in segments:
        url = f"{API_BASE}/bibles/{bible_id}/passages/{segment}"

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    text = data.get('data', {}).get('content', '')
                    text = re.sub(r'<[^>]+>', '', text)
                    texts.append(text.strip())
                    break

                elif response.status_code == 404:
                    print(f"WARNING: Passage not found: {segment} in {lang}")
                    break

                elif response.status_code == 429:
                    print(f"WARN: Rate limit hit, waiting 60s...")
                    time.sleep(60)
                    retry_count += 1
                    continue

                else:
                    print(f"ERROR: HTTP {response.status_code} for {reference}: {response.text}")
                    break

            except requests.exceptions.RequestException as e:
                    print(f"ERROR: Request failed for {segment} in {lang}: {e}")
                    break

        time.sleep(0.3)  # piccolo delay tra segmenti per non stressare l'API

    return ' '.join(texts) if texts else None


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
