#!/usr/bin/env python3
"""
Popola la tabella liturgy_proper usando i file di DivinumOfficium.

Per ogni data in liturgical_day:
  1. Cerca prima il file Sancti/MM-DD.txt (per feste/solennità)
  2. Fallback sul file Tempora corrispondente alla stagione/settimana
  3. Estrae antifone, lettura breve, colletta, ant. Benedictus/Magnificat
  4. Inserisce righe per ufficio lauds/vespers × 3 lingue (it, en, es)

DivinumOfficium: https://github.com/DivinumOfficium/divinum-officium
Percorso locale: /workspaces/divinum-officium/web/www/horas/
"""

import re
import sqlite3
from pathlib import Path

DO_ROOT = Path("/workspaces/divinum-officium/web/www/horas")
DB_PATH = Path("data/prayers.db")

LANG_MAP = {
    "it": "Italiano",
    "en": "English",
    "es": "Espanol",
}

# Cache dei file Psalterium già letti (per performance)
_psalterium_cache: dict[str, dict] = {}

# ──────────────────────────────────────────────
# Mapping stagione → prefisso file Tempora
# ──────────────────────────────────────────────

def tempora_filename(season: str, week_number: int, day_of_week: int) -> str | None:
    """
    Restituisce il nome del file Tempora da cercare.
    day_of_week: 1=Lun … 7=Dom  →  DivinumOfficium: 0=Dom, 1=Lun … 6=Sab
    """
    di_dow = day_of_week % 7  # 7→0 (Dom), 1→1 (Lun) … 6→6 (Sab)

    if season == "advent":
        w = max(1, min(week_number, 4))
        return f"Adv{w}-{di_dow}.txt"

    elif season == "christmas":
        # Settimana 1 (1-3 gen): testi simili a Epi1 (i giorni specifici sono feste → Sancti)
        # Settimana 2 (4-10 gen): domenica = Nat2-0, feriali post-Epifania = Epi1
        # Settimana 3 (11 gen, Battesimo): gestito come Epi1-0
        if week_number <= 1:
            if di_dow == 0:
                return "Nat1-0.txt"
            return f"Nat{day_of_week:02d}.txt"   # Nat01-Nat12
        elif week_number == 2:
            if di_dow == 0:
                return "Nat2-0.txt"
            # post-Epifania (Epi1 nella forma straordinaria)
            return f"Epi1-{di_dow}.txt"
        else:
            if di_dow == 0:
                return "Epi1-0.txt"
            return f"Epi1-{di_dow}.txt"

    elif season == "lent":
        if week_number == 0:
            # Mercoledì delle Ceneri e giorni seguenti → Quad1 come fallback
            return f"Quad1-{di_dow}.txt"
        w = max(1, min(week_number, 6))
        return f"Quad{w}-{di_dow}.txt"

    elif season == "easter":
        # Settimana 1 di Pasqua → Pasc0 (ottava di Pasqua nella forma straordinaria)
        pasc = week_number - 1          # settimana 1 → Pasc0, settimana 7 → Pasc6
        pasc = max(0, min(pasc, 7))
        return f"Pasc{pasc}-{di_dow}.txt"

    elif season == "ordinary":
        if week_number <= 6:
            # Tempo ordinario pre-Quaresima → settimane dopo l'Epifania (Epi)
            w = max(1, min(week_number, 6))
            return f"Epi{w}-{di_dow}.txt"
        else:
            # Tempo ordinario post-Pentecoste → Pent01-Pent24
            pent = week_number - 7      # settimana 8 → Pent01, settimana 31 → Pent24
            pent = max(1, min(pent, 24))
            return f"Pent{pent:02d}-{di_dow}.txt"

    return None


# ──────────────────────────────────────────────
# Risoluzione file
# ──────────────────────────────────────────────

def resolve_sancti(lang_dir: Path, date_str: str) -> Path | None:
    mm_dd = date_str[5:]
    p = lang_dir / "Sancti" / f"{mm_dd}.txt"
    return p if p.exists() else None


def resolve_tempora(lang_dir: Path, season: str,
                    week_number: int, day_of_week: int) -> Path | None:
    name = tempora_filename(season, week_number, day_of_week)
    if name:
        p = lang_dir / "Tempora" / name
        if p.exists():
            return p
    return None


def psalterium_sections(lang_dir: Path) -> dict:
    """Carica (con cache) il file Psalmi major.txt del Psalterium."""
    key = str(lang_dir)
    if key not in _psalterium_cache:
        p = lang_dir / "Psalterium" / "Psalmi" / "Psalmi major.txt"
        _psalterium_cache[key] = parse_sections(p) if p.exists() else {}
    return _psalterium_cache[key]


# Mapping stagione → chiave MM Capitulum nel Matutinum Special
_SEASON_MM_CAPITULUM = {
    "advent":    "MM Capitulum Adv_",
    "christmas": "MM Capitulum Nat",
    "lent":      "MM Capitulum Quad",   # settimane 1-4; per 5-6 usiamo Quad5
    "easter":    "MM Capitulum Pasch",
    "ordinary":  "MM Capitulum",
}

_matutinum_special_cache: dict[str, dict] = {}


def matutinum_special_sections(lang_dir: Path) -> dict:
    """Carica (con cache) Psalterium/Special/Matutinum Special.txt."""
    key = str(lang_dir)
    if key not in _matutinum_special_cache:
        p = lang_dir / "Psalterium" / "Special" / "Matutinum Special.txt"
        _matutinum_special_cache[key] = parse_sections(p) if p.exists() else {}
    return _matutinum_special_cache[key]


def seasonal_capitulum(lang_dir: Path, season: str, week_number: int) -> list[str]:
    """Restituisce le righe della lettura breve stagionale dal Psalterium."""
    ms = matutinum_special_sections(lang_dir)
    key = _SEASON_MM_CAPITULUM.get(season, "MM Capitulum")
    # Lent settimane 5-6 → Quad5
    if season == "lent" and week_number >= 5:
        key = "MM Capitulum Quad5"
    return ms.get(key, [])


# ──────────────────────────────────────────────
# Parsing file DivinumOfficium
# ──────────────────────────────────────────────

def parse_sections(path: Path) -> dict[str, list[str]]:
    """
    Legge un file DivinumOfficium e restituisce un dict
    { sezione_normalizzata: [righe] }
    """
    sections: dict[str, list[str]] = {}
    current = None
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1].strip()
            sections[current] = []
        elif current is not None and line:
            sections[current].append(line)
    return sections


def clean_antiphon(text: str) -> str:
    """
    Rimuove il numero di tono (;;NNN), il separatore *, e spazi extra.
    """
    text = re.sub(r";;[0-9]+", "", text)
    text = text.replace(" * ", " ").replace("* ", "")
    return text.strip()


def extract_antiphons(lines: list[str], n: int = 3) -> list[str | None]:
    """Prende le prime n antifone (una per riga)."""
    result: list[str | None] = []
    for line in lines:
        if line.startswith("!") or line.startswith("$") or line.startswith("v.") or line.startswith("V."):
            continue
        ant = clean_antiphon(line)
        if ant:
            result.append(ant)
        if len(result) == n:
            break
    while len(result) < n:
        result.append(None)
    return result


def extract_capitulum(lines: list[str]) -> tuple[str | None, str | None]:
    """Restituisce (riferimento, testo) dalla sezione Capitulum."""
    ref = None
    text = None
    for line in lines:
        if line.startswith("!"):
            ref = line[1:].strip()
        elif line.startswith("v.") or line.startswith("V."):
            t = re.sub(r"^[vV]\.\s*", "", line).strip()
            if not t.startswith("$"):
                text = t
        elif line.startswith("$"):
            break
    return ref, text


def extract_oratio(lines: list[str]) -> str | None:
    """Estrae il testo della colletta (prima della riga $)."""
    parts = []
    for line in lines:
        if line.startswith("$"):
            break
        if not line.startswith("!"):
            parts.append(line)
    text = " ".join(parts).strip()
    return text if text else None


def extract_single_antiphon(lines: list[str]) -> str | None:
    """Per [Ant 2] e [Ant 3]: prende la prima riga valida."""
    for line in lines:
        if line.startswith("!") or line.startswith("$") or line.startswith("V."):
            continue
        ant = clean_antiphon(line)
        if ant:
            return ant
    return None


def get_section(primary_secs: dict, fallback_secs: dict | None,
                *keys: str) -> list[str]:
    """Cerca la sezione in primary, poi in fallback."""
    for k in keys:
        v = primary_secs.get(k)
        if v:
            return v
    if fallback_secs:
        for k in keys:
            v = fallback_secs.get(k)
            if v:
                return v
    return []


def parse_office(lang_dir: Path, day_of_week: int,
                 primary_path: Path,
                 tempora_path: Path | None = None,
                 sunday_tempora_path: Path | None = None,
                 season: str = "ordinary",
                 week_number: int = 1) -> dict:
    """
    Estrae lauds e vespers combinando:
    1. File primario (Sancti o Tempora)
    2. Fallback al file Tempora stagionale (per collect/capitulum quando mancante)
    3. Psalterium per le antifone feriali

    day_of_week: 1=Lun … 7=Dom (per Psalterium lookup)
    """
    primary_secs = parse_sections(primary_path)
    tempora_secs = parse_sections(tempora_path) if tempora_path else {}
    sunday_tempora_secs = parse_sections(sunday_tempora_path) if sunday_tempora_path else {}
    psal_secs = psalterium_sections(lang_dir)

    # day_of_week → Day{N} nel Psalterium (0=Dom, 1=Lun…6=Sab)
    psal_day = day_of_week % 7  # 7→0 (Dom), 1→1 (Lun)…6→6 (Sab)
    psal_laudes_key = f"Day{psal_day} Laudes1"
    psal_vesp_key   = f"Day{psal_day} Vespera"

    # ── Collect (Oratio) ── primary → tempora → domenica stessa settimana
    # Alcuni file feriali (Epi, Quad) usano "Oratio 2" invece di "Oratio"
    oratio_lines = get_section(primary_secs, tempora_secs, "Oratio", "Oratio 2")
    if not oratio_lines and sunday_tempora_secs:
        oratio_lines = sunday_tempora_secs.get("Oratio", [])
    collect = extract_oratio(oratio_lines)

    # ── Lauds ──
    ant_laudes_lines = get_section(primary_secs, None, "Ant Laudes")
    if not ant_laudes_lines:
        # Psalterium fallback: antifone settimanali per il giorno
        ant_laudes_lines = psal_secs.get(psal_laudes_key, [])
    lauds_ants = extract_antiphons(ant_laudes_lines, 3)

    cap_laudes = get_section(primary_secs, tempora_secs, "Capitulum Laudes")
    if not cap_laudes:
        cap_laudes = sunday_tempora_secs.get("Capitulum Laudes", [])
    if not cap_laudes:
        cap_laudes = seasonal_capitulum(lang_dir, season, week_number)
    laudes_ref, laudes_reading = extract_capitulum(cap_laudes)

    ant2_lines = get_section(primary_secs, tempora_secs, "Ant 2")
    if not ant2_lines:
        ant2_lines = sunday_tempora_secs.get("Ant 2", [])
    benedictus_ant = extract_single_antiphon(ant2_lines)

    # ── Vespers ──
    vesp_lines = get_section(primary_secs, None, "Ant Vespera 3", "Ant Vespera")
    if not vesp_lines:
        vesp_lines = psal_secs.get(psal_vesp_key, [])
    vespers_ants = extract_antiphons(vesp_lines, 3)

    cap_vesp = get_section(primary_secs, tempora_secs, "Capitulum Vespera", "Capitulum Laudes")
    if not cap_vesp:
        cap_vesp = sunday_tempora_secs.get("Capitulum Vespera",
                   sunday_tempora_secs.get("Capitulum Laudes", []))
    if not cap_vesp:
        cap_vesp = seasonal_capitulum(lang_dir, season, week_number)
    vesp_ref, vesp_reading = extract_capitulum(cap_vesp)

    ant3_lines = get_section(primary_secs, tempora_secs, "Ant 3")
    magnificat_ant = extract_single_antiphon(ant3_lines)

    return {
        "lauds": {
            "antiphon_1": lauds_ants[0],
            "antiphon_2": lauds_ants[1],
            "antiphon_3": lauds_ants[2],
            "short_reading_ref": laudes_ref,
            "short_reading": laudes_reading,
            "collect": collect,
            "benedictus_ant": benedictus_ant,
        },
        "vespers": {
            "antiphon_1": vespers_ants[0],
            "antiphon_2": vespers_ants[1],
            "antiphon_3": vespers_ants[2],
            "short_reading_ref": vesp_ref,
            "short_reading": vesp_reading,
            "collect": collect,
            "magnificat_ant": magnificat_ant,
        },
    }


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Pulisce eventuali run precedenti
    cur.execute("DELETE FROM liturgy_proper")

    # Legge tutti i giorni dell'anno
    cur.execute("""
        SELECT date, season, week_number, day_of_week, celebration_name, celebration_type
        FROM liturgical_day
        ORDER BY date
    """)
    days = cur.fetchall()

    rows_inserted = 0
    rows_missing = 0

    for date_str, season, week_number, day_of_week, cel_name, cel_type in days:
        for lang_code, lang_dir_name in LANG_MAP.items():
            lang_dir = DO_ROOT / lang_dir_name

            is_ferial = cel_type == "ferial"
            sancti_path = None if is_ferial else resolve_sancti(lang_dir, date_str)
            tempora_path = resolve_tempora(lang_dir, season, week_number, day_of_week)

            # Determina file primario: Sancti se esiste, altrimenti Tempora
            primary_path = sancti_path or tempora_path
            if primary_path is None:
                rows_missing += 1
                continue

            # Tempora usato come fallback anche quando il primario è Sancti
            fallback_tempora = tempora_path if primary_path == sancti_path else None

            # Domenica della stessa settimana: fallback per Oratio sui feriali
            # senza colletta propria (es. Epi1-1…Epi1-6 usano l'Oratio di Epi1-0)
            sunday_tempora = None
            if day_of_week != 7:    # non è già domenica
                sun_name = tempora_filename(season, week_number, 7)  # dow=7 → 0 (Dom)
                if sun_name:
                    sun_path = lang_dir / "Tempora" / sun_name
                    if sun_path.exists():
                        sunday_tempora = sun_path

            try:
                offices = parse_office(lang_dir, day_of_week,
                                       primary_path, fallback_tempora, sunday_tempora,
                                       season, week_number)
            except Exception as e:
                print(f"  ERRORE parsing {primary_path}: {e}")
                rows_missing += 1
                continue

            for office_name, fields in offices.items():
                # Inserisci solo se c'è almeno un campo significativo
                if not any(fields.values()):
                    continue

                if office_name == "lauds":
                    cur.execute("""
                        INSERT INTO liturgy_proper
                          (date, lang, office,
                           antiphon_1, antiphon_2, antiphon_3,
                           short_reading, short_reading_ref,
                           collect, benedictus_ant)
                        VALUES (?,?,?,?,?,?,?,?,?,?)
                    """, (
                        date_str, lang_code, "lauds",
                        fields["antiphon_1"], fields["antiphon_2"], fields["antiphon_3"],
                        fields["short_reading"], fields["short_reading_ref"],
                        fields["collect"], fields["benedictus_ant"],
                    ))
                else:
                    cur.execute("""
                        INSERT INTO liturgy_proper
                          (date, lang, office,
                           antiphon_1, antiphon_2, antiphon_3,
                           short_reading, short_reading_ref,
                           collect, magnificat_ant)
                        VALUES (?,?,?,?,?,?,?,?,?,?)
                    """, (
                        date_str, lang_code, "vespers",
                        fields["antiphon_1"], fields["antiphon_2"], fields["antiphon_3"],
                        fields["short_reading"], fields["short_reading_ref"],
                        fields["collect"], fields["magnificat_ant"],
                    ))
                rows_inserted += 1

    conn.commit()
    conn.close()

    print(f"\n✓ Righe inserite: {rows_inserted}")
    print(f"  File non trovati / errori: {rows_missing}")
    total_possible = len(days) * len(LANG_MAP) * 2  # 2 uffici
    pct = rows_inserted / total_possible * 100
    print(f"  Copertura: {pct:.1f}% ({rows_inserted}/{total_possible})")


if __name__ == "__main__":
    main()
