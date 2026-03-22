#!/usr/bin/env python3
"""
Popola la tabella psalm con i 150 salmi (IT, EN, ES)
da DivinumOfficium/web/www/horas/{Lang}/Psalterium/Psalmorum/Psalm{N}.txt

Formato di ogni file:
    N:V text * text (emistichi, separati da * o †)
    ...una riga per verso...

Output: testo pulito con un verso per riga, numeri di verso mantenuti.
"""

import re
import sqlite3
from pathlib import Path

DO_ROOT = Path("/workspaces/divinum-officium/web/www/horas")
DB_PATH = Path("data/prayers.db")

LANG_MAP = {"it": "Italiano", "en": "English", "es": "Espanol"}

PSALM_TITLES = {
    "it": {
        1: "Beato l'uomo giusto", 2: "Il regno del Messia", 3: "Fiducia in Dio perseguitato",
        4: "Preghiera serale", 5: "Supplica mattutina", 6: "Penitenza nella malattia",
        7: "Supplica contro i persecutori", 8: "Grandezza di Dio e dignità dell'uomo",
        9: "Azione di grazie per la vittoria", 10: "Rifugio in Dio",
        11: "Fiducia nella parola di Dio", 12: "Supplica nella sofferenza",
        13: "La corruzione umana", 14: "Chi abita sul monte del Signore",
        15: "Dio è la mia sorte", 16: "Supplica di un innocente",
        17: "Cantico di vittoria", 18: "I cieli narrano la gloria di Dio",
        19: "Preghiera per il re", 20: "Rendimento di grazie per la vittoria",
        21: "Lamentazione e fiducia del Messia sofferente", 22: "Il Signore è il mio pastore",
        23: "Il re della gloria entra nel tempio", 24: "Supplica e fiducia",
        25: "Preghiera di un giusto perseguitato", 26: "Il Signore è mia luce e salvezza",
        27: "Supplica e fiducia in Dio", 28: "La voce del Signore sul mare",
        29: "Azione di grazie per la guarigione", 30: "Supplica nel pericolo di morte",
        31: "La felicità del peccato perdonato", 32: "Lode al Dio creatore",
        33: "Inno di lode per la bontà di Dio", 34: "Supplica contro i nemici",
        35: "La malvagità degli empi e la bontà di Dio", 36: "La sorte dei giusti e degli empi",
        37: "Supplica del peccatore ammalato", 38: "Fragilità della vita umana",
        39: "Azione di grazie e supplica", 40: "Preghiera nella malattia",
        41: "Nostalgia del tempio", 42: "Preghiera nell'esilio",
        43: "Lamento del popolo in guerra", 44: "Canto nuziale per il re",
        45: "Dio è il nostro rifugio", 46: "Il Signore re dell'universo",
        47: "Sion, città del grande Re", 48: "Vanità delle ricchezze",
        49: "Dio giudice di Israele", 50: "Miserere — Il peccatore implora perdono",
        51: "La malvagità del calunniatore", 52: "La corruzione umana",
        53: "Supplica contro i nemici", 54: "Tradimento di un amico",
        55: "Fiducia in Dio perseguitato", 56: "Supplica e lode",
        57: "Supplica contro i giudici iniqui", 58: "Supplica contro i nemici",
        59: "Lamento del popolo sconfitto", 60: "Fiducia in Dio",
        61: "Riposo nell'attesa di Dio", 62: "Desiderio di Dio",
        63: "Supplica contro i calunniatori", 64: "Inno di lode al Dio della storia",
        65: "Azione di grazie per la liberazione", 66: "Preghiera per la benedizione",
        67: "Il trionfo di Dio Salvatore", 68: "Supplica nell'afflizione",
        69: "Grido di aiuto", 70: "Fiducia di un vecchio",
        71: "Il re giusto e la pace messianica", 72: "Il problema della prosperità degli empi",
        73: "Lamento per la distruzione del tempio", 74: "Dio giudice degli empi",
        75: "Il Dio della giustizia", 76: "La grande notte della liberazione",
        77: "Meditazione sulla storia della salvezza", 78: "Preghiera per il popolo oppresso",
        79: "Supplica per la vite devastata", 80: "Supplica per la conversione",
        81: "Monito divino a Israele", 82: "Contro i giudici iniqui",
        83: "Preghiera contro i nemici di Israele", 84: "Nostalgia del tempio",
        85: "Preghiera per la salvezza del popolo", 86: "Sion, madre di tutti i popoli",
        87: "Supplica di un moribondo", 88: "Lamento per le promesse disattese",
        89: "La fragilità dell'uomo davanti a Dio eterno", 90: "Sotto la protezione di Dio",
        91: "Lode del giusto", 92: "Il Signore regna", 93: "Il Signore giudice",
        94: "Invito alla lode e all'ascolto", 95: "Il Signore viene a giudicare",
        96: "Il Signore regna", 97: "Il Signore ha vinto", 98: "Il Signore re santo",
        99: "Inno di lode all'ingresso del tempio", 100: "Il re salmista",
        101: "Supplica del povero afflitto", 102: "La misericordia paterna di Dio",
        103: "Inno al Dio creatore", 104: "Le meraviglie della storia della salvezza",
        105: "Confessione dei peccati del popolo", 106: "Azione di grazie del liberato",
        107: "Dio aiuta chi lo invoca", 108: "Supplica contro i nemici",
        109: "Il re-sacerdote messianico", 110: "Le opere di Dio",
        111: "L'uomo che teme Dio", 112: "Il Signore esalta gli umili",
        113: "L'Esodo e la vanità degli idoli", 114: "Azione di grazie per la liberazione",
        115: "Voto di riconoscenza", 116: "Lode alla bontà di Dio",
        117: "Azione di grazie per la vittoria", 118: "Lode alla legge di Dio",
        119: "Pellegrino verso il tempio", 120: "Il Signore custodisce il suo popolo",
        121: "Saluto a Gerusalemme", 122: "Supplica per la misericordia",
        123: "Il Signore nostro aiuto", 124: "Sion sotto la protezione di Dio",
        125: "Fiducia del popolo che ritorna", 126: "La casa e i figli, dono di Dio",
        127: "La famiglia benedetta da Dio", 128: "Contro i nemici di Israele",
        129: "Dal profondo grido a te", 130: "Abbandono fiducioso in Dio",
        131: "L'arca del Signore nel tempio", 132: "La fratellanza dei figli di Dio",
        133: "Benedizione notturna", 134: "Lode alla potenza di Dio",
        135: "La sua misericordia è eterna", 136: "Lamento degli esiliati",
        137: "Azione di grazie per la benevolenza di Dio", 138: "Dio conosce ogni cosa",
        139: "Supplica contro i violenti", 140: "Supplica per la protezione",
        141: "Supplica nella persecuzione", 142: "Supplica del perseguitato",
        143: "Supplica per la vittoria e la prosperità", 144: "Inno alla grandezza di Dio",
        145: "Lode al Dio liberatore", 146: "Inno a Dio che governa il mondo",
        147: "Lode a Dio che governa la natura", 148: "Lode di tutta la creazione",
        149: "Canto del nuovo popolo di Dio", 150: "Alleluia finale",
    },
    "en": {
        1: "The Two Ways", 2: "The Messianic King", 3: "Trust in God under persecution",
        22: "The Good Shepherd",
    },
    "es": {},
}


def parse_psalm_file(path: Path) -> str:
    """
    Legge un file Psalm{N}.txt e restituisce il testo pulito.
    Formato: 'N:Va text * text' — rimuove numerazione, *, †, ;;NNN
    """
    lines = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        # Rimuove numero di verso iniziale (es. "1:3a ")
        line = re.sub(r"^\d+:\d+[a-z]?\s+", "", line)
        # Rimuove tono salmodia ;;NNN
        line = re.sub(r";;[0-9]+", "", line)
        # Rimuove separatori di emistichi * e †, normalizza spazi
        line = line.replace(" * ", " ").replace("* ", "").replace(" † ", " ").replace("† ", "")
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS psalm (
            id INTEGER PRIMARY KEY,
            number INTEGER NOT NULL,
            lang TEXT NOT NULL,
            title TEXT,
            text TEXT NOT NULL
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_psalm_number_lang ON psalm(number, lang)")
    cur.execute("DELETE FROM psalm")

    inserted = 0
    missing = 0

    for lang_code, lang_dir_name in LANG_MAP.items():
        psalmorum = DO_ROOT / lang_dir_name / "Psalterium" / "Psalmorum"
        titles = PSALM_TITLES.get(lang_code, {})

        for n in range(1, 151):
            path = psalmorum / f"Psalm{n}.txt"
            if not path.exists():
                missing += 1
                continue

            text = parse_psalm_file(path)
            if not text:
                missing += 1
                continue

            title = titles.get(n)
            cur.execute(
                "INSERT INTO psalm (number, lang, title, text) VALUES (?,?,?,?)",
                (n, lang_code, title, text)
            )
            inserted += 1

    conn.commit()
    conn.close()

    print(f"✓ psalm: {inserted} righe inserite ({missing} file mancanti)")


if __name__ == "__main__":
    main()
