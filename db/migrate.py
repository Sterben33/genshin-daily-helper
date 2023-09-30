from pathlib import Path
import sqlite3
from sqlite3 import Cursor


def apply_migration(sql: str, name: str, cursor: Cursor):
    cursor.execute(sql)
    cursor.execute(f"INSERT INTO migrations (name) VALUES (?)", [name])


def migrate():
    connection = sqlite3.connect('db/sqlite.db')
    cursor = connection.cursor()
    # Ensure migrations table exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')
    connection.commit()

    last_migration = cursor.execute('''
    SELECT name FROM migrations 
    ORDER BY id DESC
    LIMIT 1;
    ''').fetchall()
    is_new = len(last_migration) == 0
    if not is_new:
        last_migration = last_migration[0]

    for file in Path('db/migrations').iterdir():
        if file.is_file():
            if is_new:
                new_migration = file.read_text()
                apply_migration(new_migration, file.name, cursor)
            elif file.name == last_migration:
                is_new = True

    connection.commit()
    connection.close()
