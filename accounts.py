import json
import os
import sqlite3
from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash


DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(__file__), "accounts.sqlite3"),
)


def _connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS user_picks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                config_key TEXT NOT NULL,
                picks TEXT NOT NULL,
                points INTEGER NOT NULL,
                submitted_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE (user_id, config_key)
            );
            """
        )
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(users)").fetchall()
        }
        if "name" not in columns:
            connection.execute("ALTER TABLE users ADD COLUMN name TEXT NOT NULL DEFAULT ''")
            connection.execute("UPDATE users SET name = email WHERE name = ''")


def create_user(name, email, password):
    normalized_email = email.strip().lower()
    with _connect() as connection:
        try:
            cursor = connection.execute(
                "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (
                    name.strip(),
                    normalized_email,
                    generate_password_hash(password),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
        except sqlite3.IntegrityError:
            return None
        return cursor.lastrowid


def authenticate(email, password):
    with _connect() as connection:
        user = connection.execute(
            "SELECT id, name, email, password_hash FROM users WHERE email = ?",
            (email.strip().lower(),),
        ).fetchone()
    if user and check_password_hash(user["password_hash"], password):
        return {"id": user["id"], "name": user["name"], "email": user["email"]}
    return None


def get_user(user_id):
    with _connect() as connection:
        user = connection.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    return dict(user) if user else None


def save_picks(user_id, config_key, picks, points):
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO user_picks (user_id, config_key, picks, points, submitted_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, config_key) DO UPDATE SET
                picks = excluded.picks,
                points = excluded.points,
                submitted_at = excluded.submitted_at
            """,
            (
                user_id,
                config_key,
                json.dumps(picks),
                points,
                datetime.now(timezone.utc).isoformat(),
            ),
        )


def get_picks(user_id, config_key):
    with _connect() as connection:
        row = connection.execute(
            "SELECT picks, points FROM user_picks WHERE user_id = ? AND config_key = ?",
            (user_id, config_key),
        ).fetchone()
    if not row:
        return None
    return {"picks": json.loads(row["picks"]), "points": row["points"]}


init_db()
