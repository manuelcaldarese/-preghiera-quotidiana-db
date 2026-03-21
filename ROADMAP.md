# ROADMAP — Preghiera Quotidiana DB

## Scopo di questa repository

Questa repo (`preghiera-quotidiana-db`) ha un unico scopo: **costruire e validare
il file SQLite `data/prayers.db`** che verrà bundled nell'app mobile Flutter.

NON è la repo dell'app. È la pipeline di dati.
L'app non farà MAI chiamate API a runtime — tutto il contenuto è pre-computato qui.

---

## L'app che verrà (repo separata: `preghiera-quotidiana-app`)

App mobile nativa Flutter, iOS + Android, 4 lingue (IT, EN, ES, PT).

### Funzionalità core
- **Home**: vangelo del giorno + santo del giorno + frase spirituale
- **Preghiere**: Padre Nostro, Ave Maria, Gloria, Credo, Atto di dolore,
  Angelus / Regina Coeli (automatico per stagione liturgica), Memorare, Salve Regina
- **Rosario completo**: tutti i 4 misteri con testo guidato decina per decina,
  con TTS opzionale
- **Liturgia delle Ore**: Lodi (mattino), Ora Media, Vespri (sera), Compieta (notte)
- **Santo del giorno**: nome, tipo festa, biografia, immagine (Wikipedia),
  messaggio di auguri onomastico personalizzato
- **Via Crucis**: 14 stazioni con meditazione, 4 lingue
- **Novene**: almeno Natale, Pentecoste, Immacolata, Divina Misericordia, San Giuseppe
- **TTS**: flutter_tts (motore nativo) per ascoltare qualsiasi preghiera
- **Condivisione**: testo del vangelo/preghiera/santo condivisibile su WhatsApp e social

### Notifiche push (tutte configurabili dall'utente)
- Mattina (ora configurabile): Vangelo del giorno
- 12:00: Angelus (o Regina Coeli nel tempo pasquale, automatico)
- Sera (ora configurabile): Rosario del giorno (tipo mistero automatico per giorno)
- Giorno configurabile: Santo del giorno con auguri onomastico
- L'utente può attivare/disattivare ogni singola notifica dalle impostazioni

### Monetizzazione
**Tier gratuito:**
- Accesso a tutti i contenuti
- AdMob banner statico in fondo a ogni schermata
- AdMob interstitial solo a fine preghiera completa (es. rosario finito, via crucis finita)
- Condivisione WhatsApp/social con firma: *"Condiviso da Preghiera Quotidiana —
  Scaricala su App Store / Google Play"*

**Tier premium (abbonamento):**
- Zero pubblicità
- Condivisione senza firma (testo pulito)
- Accesso anticipato a nuovi contenuti (novene stagionali, ecc.)
- Widget iOS/Android con vangelo del giorno

### Account / Sync
- MVP: completamente offline/locale, nessun account
- Post-MVP: Firebase Auth + Firestore per sync preferiti e impostazioni tra dispositivi

---

## Struttura completa del DB

### Tabelle esistenti nello schema

| Tabella | Contenuto | Righe attese |
|---|---|---|
| `gospel` | Vangelo + prima lettura per ogni giorno, 4 lingue | 365 × 4 = 1.460 |
| `saint` | Santo del giorno, nome, bio, 4 lingue | 365 × 4 = 1.460 |
| `prayer` | Preghiere statiche tradizionali, 4 lingue | ~17 × 4 = 68 |
| `rosary_mystery` | 20 misteri × 4 lingue | 80 |
| `liturgy_proper` | Antifone, lettura breve, colletta Lodi/Vespri | da implementare |
| `liturgical_day` | Colore liturgico, tipo celebrazione, settimana | da implementare |

### Tabelle da aggiungere allo schema

**`saint_greeting`** — messaggi di auguri onomastico
```sql
CREATE TABLE saint_greeting (
    id INTEGER PRIMARY KEY,
    saint_name TEXT NOT NULL,      -- nome canonico del santo
    lang TEXT NOT NULL,            -- it, en, es, pt
    greeting_short TEXT NOT NULL,  -- es: "Buon onomastico! Oggi è la festa di San Giuseppe..."
    greeting_long TEXT,            -- versione estesa per notifica push
    fun_fact TEXT                  -- curiosità sul santo, opzionale
);
```

**`hours_prayer`** — Liturgia delle Ore semplificata
```sql
CREATE TABLE hours_prayer (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,            -- YYYY-MM-DD
    lang TEXT NOT NULL,
    hour TEXT NOT NULL,            -- 'lauds', 'terce', 'vespers', 'compline'
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
    benedictus_magnificat TEXT,    -- Benedictus a Lodi, Magnificat a Vespri, Nunc Dimittis a Compieta
    intercessions TEXT,            -- JSON array di intenzioni
    collect TEXT
);
```

**`via_crucis`** — Via Crucis
```sql
CREATE TABLE via_crucis (
    id INTEGER PRIMARY KEY,
    station INTEGER NOT NULL,      -- 1-14
    lang TEXT NOT NULL,
    title TEXT NOT NULL,           -- es: "Prima stazione: Gesù è condannato a morte"
    meditation TEXT NOT NULL,      -- testo della meditazione
    prayer TEXT NOT NULL,          -- preghiera della stazione
    scripture_ref TEXT             -- riferimento biblico opzionale
);
```

**`novena`** — Novene
```sql
CREATE TABLE novena (
    id INTEGER PRIMARY KEY,
    novena_key TEXT NOT NULL,      -- es: 'christmas', 'pentecost', 'immaculate'
    day INTEGER NOT NULL,          -- 1-9
    lang TEXT NOT NULL,
    title TEXT NOT NULL,
    intention TEXT,
    prayer TEXT NOT NULL,
    scripture_ref TEXT
);
```

**`feast_calendar`** — calendario feste per onomastici
```sql
CREATE TABLE feast_calendar (
    id INTEGER PRIMARY KEY,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    saint_name TEXT NOT NULL,      -- nome canonico
    names_it TEXT,                 -- nomi italiani associati (JSON array)
    names_en TEXT,
    names_es TEXT,
    names_pt TEXT,
    feast_rank TEXT                -- 'solemnity', 'feast', 'memorial', 'optional'
);
```

---

## Contenuti statici da includere (non dipendenti da API)

### Preghiere aggiuntive da aggiungere alla tabella `prayer`
- Preghiera di San Francesco ("Signore, fa' di me uno strumento...")
- Preghiera alla Divina Misericordia (Coroncina)
- Preghiera del mattino
- Preghiera della sera
- Preghiera per i defunti
- Preghiera per i malati
- Esame di coscienza (versione guidata)
- Preghiera prima della Confessione
- Preghiera di ringraziamento dopo la Comunione
- Inno Te Deum

### Novene da includere
- Novena di Natale (16-24 dicembre)
- Novena di Pentecoste (dopo Ascensione)
- Novena dell'Immacolata (29 novembre - 7 dicembre)
- Novena della Divina Misericordia (Venerdì Santo - Domenica della Misericordia)
- Novena a San Giuseppe (10-18 marzo)

---

## Stato attuale (al momento di scrittura)

### ✅ Funzionante
- Schema SQL con 6 tabelle base
- `prayer`: 68 righe populate
- `rosary_mystery`: 80 righe populate
- `fetch_gospel.py`: logica fetch + cache + fallback
- `fetch_saints.py`: logica fetch + Wikipedia multilingue
- `fetch_bible.py`: fetch testo biblico da api.scripture.api.bible
- INSERT colonne corrette dopo fix (`text` non `gospel_text`, `short_bio` non `biography`)

### ❌ Bug critici da fixare PRIMA di tutto
1. **`normalize_reference` in `fetch_bible.py`** produce output API non valido:
   - Verse continuations perdono capitolo: `MAT.18-21` → deve essere `MAT.1.18-MAT.1.21`
   - Suffissi lettera non strippati: `24a` → deve essere `24`
   - Input: `"Matthew 1:16, 18-21, 24a"` → output attuale: `MAT.1.16,MAT.18-21,MAT.24a`
   - Output corretto: `MAT.1.16,MAT.1.18-MAT.1.21,MAT.1.24`
   - Casi da testare obbligatoriamente dopo il fix:
     - `"Matthew 1:16, 18-21, 24a"` → `MAT.1.16,MAT.1.18-MAT.1.21,MAT.1.24`
     - `"Luke 2:16-21"` → `LUK.2.16-LUK.2.21`
     - `"2 Samuel 7:4-5a, 12-14a, 16"` → `SA2.7.4-SA2.7.5,SA2.7.12-SA2.7.14,SA2.7.16`
     - `"Romans 4:13, 16-18, 22"` → `ROM.4.13,ROM.4.16-ROM.4.18,ROM.4.22`
     - `"John 1:19-28"` → `JHN.1.19-JHN.1.28`

2. **Tabelle `gospel` e `saint` sono vuote** — dipende dal fix del punto 1

### 🔄 Non ancora implementato
- Nuove tabelle: `saint_greeting`, `hours_prayer`, `via_crucis`, `novena`, `feast_calendar`
- Popolamento `liturgy_proper` e `liturgical_day`
- Parametro `--year YYYY` in `build_db.py`
- Script di validazione finale del DB

---

## Sequenza di comandi per Claude Code

### Comando 1 — Genera checklist operativa nel README
```
Leggi ROADMAP.md interamente. Capisci che questa repo produce un SQLite bundled
per un'app Flutter di preghiera cattolica (iOS + Android, 4 lingue).
Aggiorna README.md aggiungendo una sezione "## Checklist operativa" con tutti
gli step necessari per portare il DB allo stato "production ready", in ordine
di priorità, con checkbox [ ]. Ogni step deve essere concreto e verificabile.
Non modificare altro nel README.
```

### Comando 2 — Implementa tutto in ordine
```
Leggi ROADMAP.md e la "Checklist operativa" nel README.
Implementa ogni step uno alla volta nell'ordine indicato.
Dopo ogni step completato aggiorna la checkbox da [ ] a [x].
Se uno step fallisce, scrivi il motivo accanto alla checkbox come nota,
e prosegui con il successivo. Alla fine stampa il riepilogo.
```

### Comando 2b — Test su data singola prima del build completo
```
Prima di lanciare build_db.py per l'anno intero, testa fetch_gospel.py
e fetch_saints.py su 2026-03-19 e verifica che gospel_text_it, gospel_text_en,
gospel_text_es, gospel_text_pt siano tutti non vuoti. Solo se il test passa,
procedi con il build completo.
```

### Comando 3 — Validazione finale DB
```
Esegui query di validazione su data/prayers.db e verifica:
- gospel: >= 1460 righe, zero righe con text vuoto o NULL
- saint: >= 1460 righe, zero righe con name vuoto
- prayer: esattamente 68 righe (o più se aggiunte)
- rosary_mystery: esattamente 80 righe
- via_crucis: esattamente 56 righe (14 stazioni × 4 lingue)
- novena: controlla che ogni novena abbia esattamente 9 giorni × 4 lingue
- Stampa date mancanti in gospel (se ci sono gap nel calendario 2026)
- Stampa riepilogo finale: tabella con nome tabella, righe attese, righe reali, stato OK/KO
```

---

## Note architetturali per Claude Code

- Linguaggio: Python 3.8+, nessuna dipendenza esterna oltre a `requests` e `python-dotenv`
- DB: SQLite, path `data/prayers.db`
- Schema in: `schema.sql` — aggiornarlo quando si aggiungono tabelle
- Entry point build: `scripts/build_db.py`
- API key: `.env` → `BIBLE_API_KEY` — non committare MAI
- Rate limiting: 1 secondo obbligatorio tra chiamate a api.scripture.api.bible
- Cache raw: `data/raw/gospel/YYYY-MM-DD.json` e `data/raw/saints/YYYY-MM-DD.json`
  vanno preservati — permettono resume in caso di interruzione
- Lingue: sempre tutte e 4 (`it`, `en`, `es`, `pt`) — mai saltarne una
- Il DB finale `data/prayers.db` va committato nella repo
- I contenuti statici (preghiere, misteri, via crucis, novene) vanno scritti
  direttamente negli script Python, non fetchati da API
- I contenuti dinamici (vangelo, santi, liturgia) vengono fetchati e cachati
