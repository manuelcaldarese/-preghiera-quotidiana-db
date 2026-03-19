#!/usr/bin/env python3
import sys
import os
import datetime
import json
import time
import requests

# Lingue supportate
LANGUAGES = {
    'it': 'vangelo/giorno',
    'en': 'gospel/day',
    'es': 'evangelio/dia',
    'pt': 'evangelho/dia'
}

BASE_URL = 'https://evangeli.net'

def log_error(message):
    """Logga un errore nel file errors.log"""
    with open('data/raw/errors.log', 'a', encoding='utf-8') as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"{timestamp}: {message}\n")

def fetch_gospel_for_date(lang, date):
    """Fetcha il vangelo per una lingua e data specifica"""
    yyyy, mm, dd = date.split('-')
    url = f"{BASE_URL}/{LANGUAGES[lang]}/{yyyy}/{mm}/{dd}.json"

    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        print(f"{date} {lang}: {status}")

        if status == 200:
            # Salva il JSON grezzo
            dir_path = f"data/raw/gospel/{lang}"
            os.makedirs(dir_path, exist_ok=True)
            file_path = f"{dir_path}/{date}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
        else:
            log_error(f"HTTP {status} for {lang} {date}")

    except requests.exceptions.RequestException as e:
        print(f"{date} {lang}: ERROR - {str(e)}")
        log_error(f"Request failed for {lang} {date}: {str(e)}")

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 scripts/fetch_gospel.py <start_date> <end_date>")
        print("Esempio: python3 scripts/fetch_gospel.py 2026-01-01 2026-12-31")
        sys.exit(1)

    start_date_str = sys.argv[1]
    end_date_str = sys.argv[2]

    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Formato date non valido. Usa YYYY-MM-DD")
        sys.exit(1)

    if start_date > end_date:
        print("start_date deve essere <= end_date")
        sys.exit(1)

    # Crea directory se non esistono
    os.makedirs('data/raw/gospel', exist_ok=True)

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.isoformat()
        for lang in LANGUAGES:
            fetch_gospel_for_date(lang, date_str)
            time.sleep(1)  # Delay di 1 secondo
        current_date += datetime.timedelta(days=1)

if __name__ == '__main__':
    main()
