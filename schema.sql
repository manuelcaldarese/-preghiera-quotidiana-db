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

CREATE INDEX idx_gospel_date_lang ON gospel(date, lang);
CREATE INDEX idx_saint_date_lang ON saint(date, lang);
CREATE INDEX idx_liturgy_date_lang_office ON liturgy_proper(date, lang, office);
CREATE INDEX idx_prayer_key_lang ON prayer(key, lang);
