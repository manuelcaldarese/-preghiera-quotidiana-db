#!/usr/bin/env python3
"""
Popola la tabella hours_prayer con 4 ore liturgiche per ogni giorno:
  - lauds   (Lodi)
  - terce   (Terza)
  - vespers (Vespri)
  - compline (Compieta — statica per lingua)

Fonti:
  - lauds/vespers: dati da liturgy_proper + hymn/invitatory/responsory da DivinumOfficium
  - terce: capitulum e responsorio dall'ufficio del giorno (Tempora/Sancti)
  - compline: completamente statica da Psalterium/Special/Minor Special.txt
"""

import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from populate_liturgy_proper import (
    DO_ROOT, DB_PATH, LANG_MAP,
    resolve_sancti, resolve_tempora,
    parse_sections, extract_oratio,
    clean_antiphon,
)


# ──────────────────────────────────────────────
# Helper: join hymn lines into clean text
# ──────────────────────────────────────────────

def _join_hymn(lines: list[str]) -> str | None:
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


def extract_hymn(sections: dict) -> tuple[str | None, str | None]:
    return (
        _join_hymn(sections.get("Hymnus Laudes", [])),
        _join_hymn(sections.get("Hymnus Vespera", [])),
    )


def extract_invitatory(sections: dict) -> str | None:
    for line in sections.get("Invit", []):
        if line.startswith("$") or line.startswith("!"):
            continue
        text = clean_antiphon(line)
        if text:
            return text
    return None


def extract_responsory(sections: dict, key_candidates: list[str]) -> str | None:
    for key in key_candidates:
        lines = sections.get(key, [])
        parts = []
        for line in lines:
            if line.startswith("$") or line.startswith("&") or line.startswith("V."):
                continue
            line = line.lstrip("R. ").lstrip("R.br. ").strip().lstrip("*").strip()
            if line:
                parts.append(line)
        if parts:
            return " ".join(parts[:3])
    return None


def extract_capitulum(sections: dict, key: str) -> tuple[str | None, str | None]:
    """Restituisce (testo, riferimento) da una sezione Capitulum."""
    ref, text = None, None
    for line in sections.get(key, []):
        if line.startswith("!"):
            ref = line[1:].strip()
        elif line.startswith("v.") or line.startswith("V."):
            t = line[2:].strip()
            if not t.startswith("$"):
                text = t
        elif line.startswith("$"):
            break
    return text, ref


# ──────────────────────────────────────────────
# Compieta statica da Minor Special.txt
# ──────────────────────────────────────────────

def load_compline_static(lang_code: str) -> dict:
    lang_dir = DO_ROOT / LANG_MAP[lang_code]
    path = lang_dir / "Psalterium" / "Special" / "Minor Special.txt"
    if not path.exists():
        return {}
    secs = parse_sections(path)

    hymn = _join_hymn(secs.get("Hymnus Completorium", []))

    # Lettura breve
    reading, reading_ref = extract_capitulum(secs, "Completorium_")
    if not reading:
        # Prova [Lectio Completorium]
        for line in secs.get("Lectio Completorium", []):
            if line.startswith("!"):
                reading_ref = line[1:].strip()
            elif not line.startswith("$") and not line.startswith("!"):
                reading = line
                break

    responsory = extract_responsory(secs, ["Responsory Completorium"])

    # Antifona al Nunc Dimittis ([Ant 4])
    nunc_dimittis_ant = None
    for line in secs.get("Ant 4", []):
        if not line.startswith("$") and not line.startswith("!"):
            nunc_dimittis_ant = clean_antiphon(line)
            break

    # Antifona di apertura ([Completorium_] o [Ant Completorium])
    ant1 = None
    for line in secs.get("Completorium_", secs.get("Ant Completorium", [])):
        if line.startswith("!"):
            continue
        if line.startswith("v.") or line.startswith("V."):
            t = line[2:].strip()
            if not t.startswith("$"):
                ant1 = t
                break

    return {
        "hymn": hymn,
        "antiphon_1": ant1,
        "short_reading": reading,
        "short_reading_ref": reading_ref,
        "responsory": responsory,
        "benedictus_magnificat": nunc_dimittis_ant,  # Nunc Dimittis
    }


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

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

    # Pre-carica Compieta statica per lingua
    compline_static = {lang: load_compline_static(lang) for lang in LANG_MAP}

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
            _file_cache[cache_key] = parse_sections(primary) if primary else {}

        secs = _file_cache[cache_key]

        hymn_laudes, hymn_vespers = extract_hymn(secs)
        invitatory = extract_invitatory(secs)

        if office == "lauds":
            # ── Lodi ──
            cur.execute("""
                INSERT INTO hours_prayer
                  (date, lang, hour, invitatory, hymn,
                   antiphon_1, antiphon_2,
                   short_reading, short_reading_ref,
                   responsory, benedictus_magnificat, collect)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                date_str, lang, "lauds",
                invitatory, hymn_laudes,
                ant1, ant2,
                short_reading, short_reading_ref,
                extract_responsory(secs, ["Responsory Breve Tertia", "Responsory Breve", "Responsory1"]),
                benedictus_ant, collect,
            ))
            inserted += 1

            # ── Terza ──
            terce_reading, terce_ref = extract_capitulum(secs, "Capitulum Tertia")
            if not terce_reading:
                terce_reading, terce_ref = short_reading, short_reading_ref
            terce_resp = extract_responsory(secs, ["Responsory Breve Tertia"])

            cur.execute("""
                INSERT INTO hours_prayer
                  (date, lang, hour,
                   short_reading, short_reading_ref,
                   responsory, collect)
                VALUES (?,?,?,?,?,?,?)
            """, (
                date_str, lang, "terce",
                terce_reading, terce_ref,
                terce_resp, collect,
            ))
            inserted += 1

        else:
            # ── Vespri ──
            cur.execute("""
                INSERT INTO hours_prayer
                  (date, lang, hour, hymn,
                   antiphon_1, antiphon_2,
                   short_reading, short_reading_ref,
                   responsory, benedictus_magnificat, collect)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                date_str, lang, "vespers",
                hymn_vespers,
                ant1, ant2,
                short_reading, short_reading_ref,
                extract_responsory(secs, ["Responsory Breve Nona", "Responsory Breve"]),
                magnificat_ant, collect,
            ))
            inserted += 1

            # ── Compieta (statica per lingua, una riga per giorno) ──
            c = compline_static[lang]
            cur.execute("""
                INSERT INTO hours_prayer
                  (date, lang, hour, hymn,
                   antiphon_1,
                   short_reading, short_reading_ref,
                   responsory, benedictus_magnificat)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                date_str, lang, "compline",
                c.get("hymn"), c.get("antiphon_1"),
                c.get("short_reading"), c.get("short_reading_ref"),
                c.get("responsory"), c.get("benedictus_magnificat"),
            ))
            inserted += 1

    conn.commit()
    conn.close()

    days = len({(r[0], r[1]) for r in rows})
    print(f"✓ hours_prayer: {inserted} righe inserite"
          f" ({days} giorni × {len(LANG_MAP)} lingue × 4 ore)")


if __name__ == "__main__":
    main()
