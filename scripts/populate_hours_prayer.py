#!/usr/bin/env python3
"""
Popola la tabella hours_prayer con dati estesi rispetto a liturgy_proper:
aggiunge inno (hymn), invitatorio, responsorio.

Riusa il parsing di DivinumOfficium già implementato in populate_liturgy_proper.py.

Logica:
  - Parte dai dati già presenti in liturgy_proper (antifone, lettura, colletta)
  - Riapre i file DO per ogni data/lingua per estrarre hymn, invitatory, responsory
  - psalm_1/2_text e intercessions rimangono NULL (testi troppo grandi / generati dall'app)
  - benedictus_magnificat = antifona del Benedictus/Magnificat (stessa di liturgy_proper)
"""

import sys
import sqlite3
from pathlib import Path

# Importa helpers da populate_liturgy_proper
sys.path.insert(0, str(Path(__file__).parent))
from populate_liturgy_proper import (
    DO_ROOT, DB_PATH, LANG_MAP,
    resolve_sancti, resolve_tempora,
    parse_sections, extract_oratio,
)


def extract_hymn(sections: dict) -> tuple[str | None, str | None]:
    """Restituisce (hymn_laudes, hymn_vespers)."""
    def _join(lines):
        if not lines:
            return None
        parts = []
        for line in lines:
            if line.startswith("$") or line.startswith("!"):
                continue
            if line.startswith("v.") or line.startswith("V."):
                parts.append(line[2:].strip())
            elif line == "_":
                parts.append("\n")
            else:
                parts.append(line)
        text = " ".join(p for p in parts if p != "\n").strip()
        return text if text else None

    laudes  = _join(sections.get("Hymnus Laudes", []))
    vespera = _join(sections.get("Hymnus Vespera", []))
    return laudes, vespera


def extract_invitatory(sections: dict) -> str | None:
    lines = sections.get("Invit", [])
    for line in lines:
        if line.startswith("$") or line.startswith("!"):
            continue
        from populate_liturgy_proper import clean_antiphon
        text = clean_antiphon(line)
        if text:
            return text
    return None


def extract_responsory(sections: dict, office: str) -> str | None:
    """Estrae il responsorio breve per l'ufficio indicato."""
    # Prova le chiavi in ordine di preferenza
    if office == "lauds":
        candidates = ["Responsory Breve Tertia", "Responsory Breve", "Responsory1"]
    else:
        candidates = ["Responsory Breve Nona", "Responsory Breve", "Responsory1"]

    for key in candidates:
        lines = sections.get(key, [])
        parts = []
        for line in lines:
            if line.startswith("$") or line.startswith("&") or line.startswith("V."):
                continue
            line = line.lstrip("R. ").lstrip("R.br. ").strip()
            if line.startswith("*"):
                line = line[1:].strip()
            if line:
                parts.append(line)
        if parts:
            return " ".join(parts[:3])  # max 3 frammenti
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Crea tabella se non esiste (nel caso si esegua standalone senza build_db)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hours_prayer (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            lang TEXT NOT NULL,
            hour TEXT NOT NULL,
            invitatory TEXT,
            hymn TEXT,
            antiphon_1 TEXT,
            psalm_1_ref TEXT,
            psalm_1_text TEXT,
            antiphon_2 TEXT,
            psalm_2_ref TEXT,
            psalm_2_text TEXT,
            short_reading TEXT,
            short_reading_ref TEXT,
            responsory TEXT,
            benedictus_magnificat TEXT,
            intercessions TEXT,
            collect TEXT
        )
    """)
    cur.execute("DELETE FROM hours_prayer")

    # Carica tutti i dati già in liturgy_proper
    cur.execute("""
        SELECT lp.date, lp.lang, lp.office,
               lp.antiphon_1, lp.antiphon_2,
               lp.short_reading, lp.short_reading_ref,
               lp.collect,
               lp.benedictus_ant, lp.magnificat_ant,
               ld.season, ld.week_number, ld.day_of_week, ld.celebration_type
        FROM liturgy_proper lp
        JOIN liturgical_day ld ON lp.date = ld.date
        ORDER BY lp.date, lp.lang, lp.office
    """)
    rows = cur.fetchall()

    inserted = 0
    # Cache file DO per (date, lang)
    _file_cache: dict[tuple, dict] = {}

    for (date_str, lang, office,
         ant1, ant2,
         short_reading, short_reading_ref,
         collect,
         benedictus_ant, magnificat_ant,
         season, week_number, day_of_week, cel_type) in rows:

        cache_key = (date_str, lang)
        if cache_key not in _file_cache:
            lang_dir = DO_ROOT / LANG_MAP[lang]
            is_ferial = cel_type == "ferial"
            sancti = None if is_ferial else resolve_sancti(lang_dir, date_str)
            tempora = resolve_tempora(lang_dir, season, week_number, day_of_week)
            primary = sancti or tempora
            if primary is None:
                _file_cache[cache_key] = {}
            else:
                try:
                    _file_cache[cache_key] = parse_sections(primary)
                except Exception:
                    _file_cache[cache_key] = {}

        secs = _file_cache[cache_key]

        hymn_laudes, hymn_vespers = extract_hymn(secs)
        invitatory  = extract_invitatory(secs)
        responsory  = extract_responsory(secs, office)

        if office == "lauds":
            hymn = hymn_laudes
            bened_magn = benedictus_ant
            hour = "lauds"
        else:
            hymn = hymn_vespers
            bened_magn = magnificat_ant
            hour = "vespers"

        cur.execute("""
            INSERT INTO hours_prayer
              (date, lang, hour,
               invitatory, hymn,
               antiphon_1, antiphon_2,
               short_reading, short_reading_ref,
               responsory, benedictus_magnificat,
               collect)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            date_str, lang, hour,
            invitatory, hymn,
            ant1, ant2,
            short_reading, short_reading_ref,
            responsory, bened_magn,
            collect,
        ))
        inserted += 1

    conn.commit()
    conn.close()

    total_possible = len({(r[0], r[1]) for r in rows}) * 2
    pct = inserted / total_possible * 100 if total_possible else 0
    print(f"✓ hours_prayer: {inserted} righe inserite ({pct:.0f}% dei giorni × lingue × uffici)")


if __name__ == "__main__":
    main()
