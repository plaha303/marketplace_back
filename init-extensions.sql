-- init-extensions.sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Створення текстової пошукової конфігурації для української мови
CREATE TEXT SEARCH CONFIGURATION ukrainian (
    COPY = simple
);

ALTER TEXT SEARCH CONFIGURATION ukrainian
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
    WITH unaccent, simple;