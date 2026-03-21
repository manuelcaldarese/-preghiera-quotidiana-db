CREATE TABLE liturgical_day (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    season TEXT NOT NULL,
    week_number INTEGER,
    day_of_week INTEGER,
    celebration_name TEXT,
    celebration_type TEXT,
    liturgical_color TEXT,
    is_sunday INTEGER DEFAULT 0,
    is_holy_day INTEGER DEFAULT 0
);

CREATE TABLE gospel (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    lang TEXT NOT NULL,
    reference TEXT,
    title TEXT,
    text TEXT NOT NULL,
    reading_1_ref TEXT,
    reading_1_text TEXT,
    psalm_ref TEXT,
    psalm_text TEXT,
    source TEXT
);

CREATE TABLE saint (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    lang TEXT NOT NULL,
    name TEXT NOT NULL,
    feast_type TEXT,
    short_bio TEXT,
    wikipedia_url TEXT
);

CREATE TABLE liturgy_proper (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    lang TEXT NOT NULL,
    office TEXT NOT NULL,
    antiphon_1 TEXT,
    antiphon_2 TEXT,
    antiphon_3 TEXT,
    short_reading TEXT,
    short_reading_ref TEXT,
    collect TEXT,
    benedictus_ant TEXT,
    magnificat_ant TEXT
);

CREATE TABLE prayer (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL,
    lang TEXT NOT NULL,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    audio_tts_hint TEXT
);

CREATE TABLE rosary_mystery (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    number INTEGER NOT NULL,
    lang TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    scripture_ref TEXT,
    recommended_days TEXT
);

CREATE TABLE via_crucis (
    id INTEGER PRIMARY KEY,
    station INTEGER NOT NULL,
    lang TEXT NOT NULL,
    title TEXT NOT NULL,
    meditation TEXT NOT NULL,
    prayer TEXT NOT NULL,
    scripture_ref TEXT
);

CREATE TABLE novena (
    id INTEGER PRIMARY KEY,
    novena_key TEXT NOT NULL,
    day INTEGER NOT NULL,
    lang TEXT NOT NULL,
    title TEXT NOT NULL,
    intention TEXT,
    prayer TEXT NOT NULL,
    scripture_ref TEXT
);

CREATE TABLE feast_calendar (
    id INTEGER PRIMARY KEY,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    saint_name TEXT NOT NULL,
    names_it TEXT,
    names_en TEXT,
    names_es TEXT,
    names_pt TEXT,
    feast_rank TEXT
);

CREATE TABLE saint_greeting (
    id INTEGER PRIMARY KEY,
    saint_name TEXT NOT NULL,
    lang TEXT NOT NULL,
    greeting_short TEXT NOT NULL,
    greeting_long TEXT,
    fun_fact TEXT
);

CREATE INDEX idx_gospel_date_lang ON gospel(date, lang);
CREATE INDEX idx_saint_date_lang ON saint(date, lang);
CREATE INDEX idx_liturgy_date_lang_office ON liturgy_proper(date, lang, office);
CREATE INDEX idx_prayer_key_lang ON prayer(key, lang);
CREATE INDEX idx_feast_calendar_month_day ON feast_calendar(month, day);
CREATE INDEX idx_saint_greeting_name_lang ON saint_greeting(saint_name, lang);
