CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    tg_id INTEGER,
    name VARCHAR,
    ltuid INTEGER NULL,
    itoken VARCHAR
)