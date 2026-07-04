import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "research_history.db"


def initialize_database() -> None:
    """Create the research_history table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS research_history (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                query    TEXT    NOT NULL,
                summary  TEXT    NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_search(query: str, summary: dict) -> None:
    """Persist a query and its summary (stored as JSON) to the DB."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO research_history (query, summary) VALUES (?, ?)",
            (query, json.dumps(summary)),
        )
        conn.commit()


def get_history(limit: int = 10) -> list[dict]:
    """Return the most recent `limit` searches, newest first."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT id, query, created_at FROM research_history ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]
