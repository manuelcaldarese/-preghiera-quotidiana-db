#!/usr/bin/env python3
"""
Validazione finale del database prayers.db.
Stampa una tabella con righe attese / righe reali / stato OK-KO per ogni tabella,
più controlli di qualità sui dati.
"""

import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path("data/prayers.db")

LANGS = ("it", "en", "es", "pt")
LANGS_3 = ("it", "en", "es")   # tabelle senza pt

EXPECTED = {
    "gospel":         365 * 4,
    "saint":          365 * 4,
    "prayer":         None,     # variabile, solo ≥ 68
    "rosary_mystery": 80,
    "via_crucis":     56,
    "novena":         None,     # variabile, solo ≥ 180
    "liturgical_day": 365,
    "liturgy_proper": 365 * 3 * 2,
    "feast_calendar": None,     # variabile
    "saint_greeting": None,     # variabile
    "hours_prayer":   365 * 3 * 2,
}

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def ok(msg="OK"):   return f"{GREEN}✓ {msg}{RESET}"
def fail(msg="KO"): return f"{RED}✗ {msg}{RESET}"
def warn(msg):      return f"{YELLOW}⚠ {msg}{RESET}"


def all_2026_dates():
    d = date(2026, 1, 1)
    end = date(2026, 12, 31)
    while d <= end:
        yield d.isoformat()
        d += timedelta(days=1)


def main():
    if not DB_PATH.exists():
        print(fail(f"DB non trovato: {DB_PATH}"))
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    tables = {r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}

    errors = 0
    warnings = 0

    print(f"\n{BOLD}{'─'*68}{RESET}")
    print(f"{BOLD}{'Tabella':<22} {'Attese':>8} {'Reali':>8}  Stato{RESET}")
    print(f"{'─'*68}")

    for table, expected in EXPECTED.items():
        if table not in tables:
            print(f"{table:<22} {str(expected or '—'):>8} {'—':>8}  {fail('tabella assente')}")
            errors += 1
            continue

        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

        if expected is None:
            # Solo controllo che non sia vuota
            status = ok() if count > 0 else fail("vuota")
            if count == 0:
                errors += 1
            print(f"{table:<22} {'—':>8} {count:>8}  {status}")
        else:
            ok_str = ok() if count >= expected else fail(f"mancano {expected - count}")
            if count < expected:
                errors += 1
            print(f"{table:<22} {expected:>8} {count:>8}  {ok_str}")

    print(f"{'─'*68}\n")

    # ── Controlli qualità ──────────────────────────────────────────

    print(f"{BOLD}Controlli qualità{RESET}")
    print(f"{'─'*68}")

    checks = []

    # gospel: zero testi vuoti
    if "gospel" in tables:
        n = cur.execute("SELECT COUNT(*) FROM gospel WHERE text IS NULL OR text=''").fetchone()[0]
        checks.append(("gospel.text mai vuoto", n == 0, f"{n} righe con testo vuoto"))

        # copertura lingue
        for lang in LANGS:
            n = cur.execute("SELECT COUNT(*) FROM gospel WHERE lang=?", (lang,)).fetchone()[0]
            checks.append((f"gospel lang={lang}", n == 365, f"{n}/365 giorni"))

        # gap nel calendario
        dates_in_db = {r[0] for r in cur.execute("SELECT DISTINCT date FROM gospel WHERE lang='it'").fetchall()}
        missing = [d for d in all_2026_dates() if d not in dates_in_db]
        checks.append(("gospel: nessun gap 2026", len(missing) == 0,
                        f"{len(missing)} date mancanti: {missing[:5]}{'…' if len(missing)>5 else ''}"))

    # saint: zero nomi vuoti
    if "saint" in tables:
        n = cur.execute("SELECT COUNT(*) FROM saint WHERE name IS NULL OR name=''").fetchone()[0]
        checks.append(("saint.name mai vuoto", n == 0, f"{n} righe senza nome"))

    # prayer: ≥ 68 righe, tutte le lingue presenti
    if "prayer" in tables:
        for lang in LANGS:
            n = cur.execute("SELECT COUNT(*) FROM prayer WHERE lang=?", (lang,)).fetchone()[0]
            checks.append((f"prayer lang={lang}", n >= 17, f"{n} preghiere"))

    # liturgy_proper: copertura e campi critici
    if "liturgy_proper" in tables:
        n_null_ant = cur.execute("SELECT COUNT(*) FROM liturgy_proper WHERE antiphon_1 IS NULL").fetchone()[0]
        checks.append(("liturgy_proper.antiphon_1 mai NULL", n_null_ant == 0, f"{n_null_ant} NULL"))

        n_null_read = cur.execute("SELECT COUNT(*) FROM liturgy_proper WHERE short_reading IS NULL").fetchone()[0]
        checks.append(("liturgy_proper.short_reading mai NULL", n_null_read == 0, f"{n_null_read} NULL"))

        n_null_col = cur.execute("SELECT COUNT(*) FROM liturgy_proper WHERE collect IS NULL").fetchone()[0]
        pct = n_null_col / (365*3*2) * 100
        checks.append(("liturgy_proper.collect < 1% NULL", pct < 1,
                        f"{n_null_col} NULL ({pct:.1f}%)"))

        for lang in LANGS_3:
            n = cur.execute("SELECT COUNT(*) FROM liturgy_proper WHERE lang=?", (lang,)).fetchone()[0]
            checks.append((f"liturgy_proper lang={lang}", n == 365*2, f"{n}/{365*2}"))

    # novena: ogni novena ha 9 giorni × 4 lingue
    if "novena" in tables:
        keys = [r[0] for r in cur.execute("SELECT DISTINCT novena_key FROM novena").fetchall()]
        for k in keys:
            for lang in LANGS:
                n = cur.execute(
                    "SELECT COUNT(DISTINCT day) FROM novena WHERE novena_key=? AND lang=?",
                    (k, lang)
                ).fetchone()[0]
                checks.append((f"novena {k}/{lang} 9 giorni", n == 9, f"{n}/9 giorni"))

    # rosary: 4 tipi × 5 misteri × 4 lingue
    if "rosary_mystery" in tables:
        types = [r[0] for r in cur.execute("SELECT DISTINCT type FROM rosary_mystery").fetchall()]
        checks.append(("rosary: 4 tipi", len(types) == 4, f"tipi: {types}"))

    # via_crucis: 14 stazioni × 4 lingue
    if "via_crucis" in tables:
        for lang in LANGS:
            n = cur.execute("SELECT COUNT(*) FROM via_crucis WHERE lang=?", (lang,)).fetchone()[0]
            checks.append((f"via_crucis lang={lang} 14 stazioni", n == 14, f"{n}/14"))

    # liturgical_day: 365 giorni, date univoche
    if "liturgical_day" in tables:
        n_dup = cur.execute(
            "SELECT COUNT(*) FROM (SELECT date, COUNT(*) c FROM liturgical_day GROUP BY date HAVING c>1)"
        ).fetchone()[0]
        checks.append(("liturgical_day: no duplicati", n_dup == 0, f"{n_dup} duplicati"))

    # Stampa risultati
    for label, passed, detail in checks:
        if passed:
            print(f"  {ok():12}  {label}")
        else:
            print(f"  {fail():12}  {label}  ({detail})")
            errors += 1

    # ── Riepilogo ──────────────────────────────────────────────────
    print(f"\n{'─'*68}")
    if errors == 0 and warnings == 0:
        print(f"{GREEN}{BOLD}✓ DB production-ready — tutti i controlli superati{RESET}")
    elif errors == 0:
        print(f"{YELLOW}{BOLD}⚠ DB quasi production-ready — {warnings} avviso/i{RESET}")
    else:
        print(f"{RED}{BOLD}✗ {errors} errore/i trovati{RESET}")

    conn.close()
    sys.exit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
