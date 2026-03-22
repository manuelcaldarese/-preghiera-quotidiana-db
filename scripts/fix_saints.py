#!/usr/bin/env python3
"""
Corregge i dati dei santi nei file raw JSON e nel DB:

PROBLEMA 1 — Nomi ES/PT in inglese:
  calapi.inadiutorium.cz supporta solo IT e EN, quindi name_es e name_pt
  vengono copiati da name_en. Questo script li corregge usando:
  1. Il titolo della pagina Wikipedia in quella lingua (via langlinks API)
  2. Fallback: deep-translator (Google Translate)

PROBLEMA 2 — Bio in lingua sbagliata (55/60 bio IT/ES/PT sono in inglese):
  Wikipedia restituisce la bio in EN e la copia su tutte le lingue.
  Questo script recupera la bio dalla pagina Wikipedia nella lingua corretta.

PROBLEMA 3 — Bio mancante per 104 santi-persone:
  Tenta una ricerca migliorata su Wikipedia in ogni lingua.
  Fallback: traduce la bio EN con deep-translator.
"""

import json
import re
import sqlite3
import time
from pathlib import Path

import requests
from deep_translator import GoogleTranslator

RAW_DIR = Path("data/raw/saints")
DB_PATH  = Path("data/prayers.db")
HEADERS  = {"User-Agent": "PreghieraQuotidiana/1.0 (liturgical-db-builder; educational)"}
LANGS    = ["it", "es", "pt"]
DELAY    = 0.5   # secondi tra chiamate Wikipedia


# ──────────────────────────────────────────────
# Wikipedia helpers
# ──────────────────────────────────────────────

def _get(url: str, params: dict = None) -> dict | None:
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if r.status_code == 429:
            print("    ⚠ rate limit Wikipedia, attendo 30s...")
            time.sleep(30)
            r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if r.ok:
            return r.json()
    except Exception:
        pass
    return None


def wiki_summary(lang: str, title: str) -> tuple[str, str]:
    """(bio, url) dalla REST API di Wikipedia."""
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}"
    data = _get(url)
    if not data or data.get("type") in ("disambiguation", "https://mediawiki.org/wiki/HyperSwitch/errors/not_found"):
        return "", ""
    bio = data.get("extract", "")
    page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
    return bio, page_url


def wiki_langlinks(en_title: str, target_langs: list[str]) -> dict[str, str]:
    """
    Dato un titolo EN Wikipedia, restituisce {lang: titolo_in_quella_lingua}.
    Usa l'API w/api.php con prop=langlinks.
    """
    params = {
        "action": "query",
        "titles": en_title,
        "prop": "langlinks",
        "lllang": "|".join(target_langs),
        "format": "json",
        "redirects": 1,
    }
    data = _get("https://en.wikipedia.org/w/api.php", params)
    if not data:
        return {}
    pages = data.get("query", {}).get("pages", {})
    result = {}
    for page in pages.values():
        for ll in page.get("langlinks", []):
            if ll.get("lang") in target_langs:
                result[ll["lang"]] = ll.get("*", "")
    return result


def wiki_search(lang: str, query: str) -> tuple[str, str]:
    """Cerca su Wikipedia in una lingua, restituisce (bio, url) del primo risultato."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 3,
        "format": "json",
    }
    data = _get(f"https://{lang}.wikipedia.org/w/api.php", params)
    if not data:
        return "", ""
    results = data.get("query", {}).get("search", [])
    for r in results:
        title = r.get("title", "")
        if not title:
            continue
        bio, url = wiki_summary(lang, title)
        time.sleep(DELAY)
        if bio and len(bio) > 50:
            return bio, url
    return "", ""


def extract_en_title(wikipedia_url_en: str) -> str | None:
    """Estrae il titolo Wikipedia dall'URL EN (es. '/wiki/Anthony_the_Great')."""
    if not wikipedia_url_en:
        return None
    m = re.search(r"/wiki/(.+)$", wikipedia_url_en)
    return m.group(1) if m else None


# ──────────────────────────────────────────────
# Traduzione con deep-translator
# ──────────────────────────────────────────────

_translators: dict[str, GoogleTranslator] = {}

def translate(text: str, target_lang: str) -> str:
    if not text or not text.strip():
        return text
    lang_map = {"it": "it", "es": "es", "pt": "pt"}
    tgt = lang_map.get(target_lang, target_lang)
    if tgt not in _translators:
        _translators[tgt] = GoogleTranslator(source="en", target=tgt)
    try:
        # deep-translator ha un limite di ~5000 caratteri per chiamata
        if len(text) <= 4900:
            return _translators[tgt].translate(text) or text
        # Testo lungo: spezza per frase
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks, cur = [], ""
        for s in sentences:
            if len(cur) + len(s) + 1 < 4900:
                cur = (cur + " " + s).strip()
            else:
                if cur:
                    chunks.append(cur)
                cur = s
        if cur:
            chunks.append(cur)
        translated = []
        for chunk in chunks:
            t = _translators[tgt].translate(chunk) or chunk
            translated.append(t)
            time.sleep(0.3)
        return " ".join(translated)
    except Exception as e:
        print(f"    ⚠ traduzione fallita ({target_lang}): {e}")
        return text


# ──────────────────────────────────────────────
# Fix di un singolo file JSON
# ──────────────────────────────────────────────

_SKIP_PATTERNS = [
    "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
    "feria", "ordinary time", "week", "easter", "lent", "advent", "christmas",
    "pentecost", "triduum", "octave", "the most holy", "the holy",
    "immaculate heart", "sacred heart", "our lord", "our lady",
    "the nativity", "the epiphany", "the baptism", "the presentation",
    "the transfiguration", "the assumption", "the exaltation",
    "corpus christi", "ash wednesday", "palm sunday", "good friday",
    "holy saturday", "all saints", "all souls", "solemnity",
]

def is_person(name: str) -> bool:
    lo = name.lower()
    return not any(p in lo for p in _SKIP_PATTERNS)


def fix_record(data: dict) -> tuple[dict, bool]:
    """
    Corregge name_{lang} e bio_{lang} per IT, ES, PT.
    Restituisce (data_aggiornato, modificato).
    """
    modified = False
    name_en  = data.get("name_en", "")
    bio_en   = data.get("bio_en", "")
    url_en   = data.get("wikipedia_url_en", "")
    en_title = extract_en_title(url_en)

    # ── Langlinks Wikipedia ──────────────────────────────────────────────
    langlinks: dict[str, str] = {}
    if en_title and is_person(name_en):
        langlinks = wiki_langlinks(en_title, LANGS)
        time.sleep(DELAY)

    for lang in LANGS:
        cur_name = data.get(f"name_{lang}", "")
        cur_bio  = data.get(f"bio_{lang}", "")
        cur_url  = data.get(f"wikipedia_url_{lang}", "")

        # ── Nome ────────────────────────────────────────────────────────
        # Fallback chain per il nome:
        # 1. Titolo Wikipedia in quella lingua (langlinks)  ← migliore
        # 2. Traduzione deep-translator di name_en          ← ok
        # 3. Mantieni il valore attuale                     ← ultimo resort
        if cur_name == name_en and name_en and is_person(name_en):
            if lang in langlinks and langlinks[lang]:
                # Il titolo Wikipedia è la forma canonica del nome
                new_name = langlinks[lang].replace("_", " ")
                data[f"name_{lang}"] = new_name
                modified = True
                print(f"    ✓ nome {lang}: {name_en!r} → {new_name!r} (langlink)")
            else:
                new_name = translate(name_en, lang)
                if new_name != name_en:
                    data[f"name_{lang}"] = new_name
                    modified = True
                    print(f"    ✓ nome {lang}: {name_en!r} → {new_name!r} (tradotto)")
            time.sleep(0.3)

        # ── Bio ─────────────────────────────────────────────────────────
        needs_bio_fix = (not cur_bio) or (cur_bio == bio_en and bio_en)

        if needs_bio_fix and is_person(name_en):
            # 1. Wikipedia nella lingua target
            if lang in langlinks and langlinks[lang]:
                new_bio, new_url = wiki_summary(lang, langlinks[lang])
                time.sleep(DELAY)
                if new_bio:
                    data[f"bio_{lang}"] = new_bio
                    data[f"wikipedia_url_{lang}"] = new_url or cur_url
                    modified = True
                    print(f"    ✓ bio  {lang}: Wikipedia [{lang}] ({len(new_bio)} chars)")
                    continue

            # 2. Ricerca Wikipedia in quella lingua (se non c'era EN Wikipedia)
            if not bio_en and not en_title:
                search_q = data.get(f"name_{lang}", name_en)
                new_bio, new_url = wiki_search(lang, search_q)
                if new_bio:
                    data[f"bio_{lang}"] = new_bio
                    data[f"wikipedia_url_{lang}"] = new_url
                    modified = True
                    print(f"    ✓ bio  {lang}: ricerca Wikipedia ({len(new_bio)} chars)")
                    continue

            # 3. Traduzione della bio EN
            if bio_en:
                new_bio = translate(bio_en, lang)
                if new_bio and new_bio != bio_en:
                    data[f"bio_{lang}"] = new_bio
                    modified = True
                    print(f"    ✓ bio  {lang}: tradotta ({len(new_bio)} chars)")

    return data, modified


# ──────────────────────────────────────────────
# Aggiorna il DB dalla cache corretta
# ──────────────────────────────────────────────

def rebuild_saint_table():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("DELETE FROM saint")

    raw_files = sorted(RAW_DIR.glob("*.json"))
    rows = []
    for path in raw_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        date_str = data.get("date")
        for lang in ["it", "en", "es", "pt"]:
            name      = data.get(f"name_{lang}", "")
            bio       = data.get(f"bio_{lang}", "")
            feat_type = data.get(f"feast_type_{lang}", "")
            wiki_url  = data.get(f"wikipedia_url_{lang}", "")
            rows.append((date_str, lang, name, feat_type, bio, wiki_url))

    cur.executemany(
        "INSERT INTO saint (date, lang, name, feast_type, short_bio, wikipedia_url) VALUES (?,?,?,?,?,?)",
        rows,
    )
    conn.commit()
    conn.close()
    print(f"\n✓ saint: {len(rows)} righe reinserite nel DB")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    raw_files = sorted(RAW_DIR.glob("*.json"))
    total = len(raw_files)
    fixed = 0

    print(f"Analisi di {total} file raw saints...\n")

    for i, path in enumerate(raw_files, 1):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ✗ {path.name}: errore lettura ({e})")
            continue

        name_en = data.get("name_en", "")
        # Skip eventi liturgici non-persone
        if not is_person(name_en):
            continue

        needs_fix = False
        for lang in LANGS:
            if data.get(f"name_{lang}") == name_en:
                needs_fix = True
            bio = data.get(f"bio_{lang}", "")
            bio_en = data.get("bio_en", "")
            if not bio or (bio == bio_en and bio_en):
                needs_fix = True

        if not needs_fix:
            continue

        print(f"[{i}/{total}] {path.stem} — {name_en}")
        new_data, modified = fix_record(data)
        if modified:
            path.write_text(json.dumps(new_data, ensure_ascii=False, indent=2), encoding="utf-8")
            fixed += 1

    print(f"\n{'─'*60}")
    print(f"File corretti: {fixed}/{total}")
    print("\nRicostruzione tabella saint nel DB...")
    rebuild_saint_table()


if __name__ == "__main__":
    main()
