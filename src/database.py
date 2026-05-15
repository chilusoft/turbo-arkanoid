import sqlite3
import os
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "game.db"


class GameDatabase:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL DEFAULT 'Player',
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                date TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL DEFAULT 'Player',
                level_unlocked INTEGER NOT NULL DEFAULT 1,
                timestamp TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def get_high_scores(self, limit=10):
        cur = self.conn.execute(
            "SELECT player_name, score, level, date FROM high_scores ORDER BY score DESC LIMIT ?",
            (limit,),
        )
        return [dict(r) for r in cur.fetchall()]

    def add_high_score(self, player_name, score, level):
        self.conn.execute(
            "INSERT INTO high_scores (player_name, score, level, date) VALUES (?, ?, ?, ?)",
            (player_name, score, level, datetime.now().isoformat()),
        )
        self.conn.commit()

    def get_progress(self, player_name="Player"):
        cur = self.conn.execute(
            "SELECT level_unlocked FROM progress WHERE player_name = ? ORDER BY id DESC LIMIT 1",
            (player_name,),
        )
        row = cur.fetchone()
        return row["level_unlocked"] if row else 1

    def save_progress(self, level, player_name="Player"):
        cur = self.conn.execute(
            "SELECT level_unlocked FROM progress WHERE player_name = ? ORDER BY id DESC LIMIT 1",
            (player_name,),
        )
        row = cur.fetchone()
        current = row["level_unlocked"] if row else 0
        if level > current:
            self.conn.execute(
                "INSERT INTO progress (player_name, level_unlocked, timestamp) VALUES (?, ?, ?)",
                (player_name, level, datetime.now().isoformat()),
            )
            self.conn.commit()

    def get_setting(self, key, default=None):
        cur = self.conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cur.fetchone()
        return row["value"] if row else default

    def set_setting(self, key, value):
        self.conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value))
        )
        self.conn.commit()

    def export_to_excel(self, filepath):
        import pandas as pd
        tables = {}
        for table in ("high_scores", "progress", "settings"):
            df = pd.read_sql(f"SELECT * FROM {table}", self.conn)
            tables[table] = df
        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            for name, df in tables.items():
                df.to_excel(writer, sheet_name=name, index=False)

    def import_from_excel(self, filepath):
        import pandas as pd
        xls = pd.ExcelFile(filepath, engine="openpyxl")
        for sheet in xls.sheet_names:
            if sheet not in ("high_scores", "progress", "settings"):
                continue
            df = pd.read_excel(xls, sheet_name=sheet)
            if df.empty:
                continue
            existing = pd.read_sql(f"SELECT * FROM {sheet}", self.conn)
            combined = pd.concat([existing, df], ignore_index=True)
            if sheet == "high_scores":
                combined = combined.drop_duplicates(subset=["player_name", "score", "level"]).sort_values("score", ascending=False)
            elif sheet == "progress":
                combined = combined.drop_duplicates(subset=["player_name"], keep="last")
            elif sheet == "settings":
                combined = combined.drop_duplicates(subset=["key"], keep="last")
            combined.to_sql(sheet, self.conn, if_exists="replace", index=False)
        self.conn.commit()

    def close(self):
        self.conn.close()
