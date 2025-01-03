"""Storage backend for Celery Admin"""
import json
import pathlib
import sqlite3
from abc import ABC, abstractmethod
from typing import Any


class Storage(ABC):
    """Abstract Storage class"""

    @abstractmethod
    def store_event(self, event: dict) -> None:
        """Method to store event info"""
        pass

    @abstractmethod
    def get_events(self) -> list[dict]:
        """Method to get events"""
        pass

    @abstractmethod
    def get_event_by_id(self, id: str) -> dict | None:
        """Method to get single event by its ID"""
        pass


class SQLiteStorage(Storage):
    """SQLite Backend"""

    def __init__(self, path: str) -> None:
        """Initializes SQLite Storage"""
        self.path = str(pathlib.Path(path).resolve())
        self.table_name = "events"

        with self._get_connection() as con:
            cursor = con.cursor()
            cursor.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        uuid TEXT,
                        data JSON,
                        name TEXT GENERATED ALWAYS AS (json_extract(data, '$.name')) VIRTUAL,
                        sent_timestamp REAL GENERATED ALWAYS AS (json_extract(data, '$.sent_timestamp')) VIRTUAL,
                    PRIMARY KEY (uuid)
                    )
                """
            )
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_name ON {self.table_name} (name)")
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_sent_timestamp ON {self.table_name} (sent_timestamp)")

    def _get_connection(self) -> Any:
        return sqlite3.connect(self.path)

    def store_event(self, event: dict) -> None:
        """Stores event info"""
        with self._get_connection() as con:
            cursor = con.cursor()
            cursor.execute(f"SELECT data FROM {self.table_name} WHERE uuid = ?", (event["uuid"],))
            row = cursor.fetchone()

            if row:
                # Record exists, merge existing data with new data
                data = json.loads(row[0])
                data.update(event)
                cursor.execute(
                    f"UPDATE {self.table_name} SET data = ? WHERE uuid = ?", (json.dumps(data), event["uuid"])
                )
            else:
                # Record does not exist, insert a new one
                cursor.execute(
                    f"INSERT INTO {self.table_name} (uuid, data) VALUES (?, ?)", (event["uuid"], json.dumps(event))
                )

    def get_events(self) -> list[dict]:
        """Gets events as list of dicts"""
        with self._get_connection() as con:
            cursor = con.cursor()
            cursor.execute(f"SELECT data FROM {self.table_name} ORDER BY sent_timestamp DESC")
            rows = cursor.fetchall()
            return [json.loads(row[0]) for row in rows]

    def get_event_by_id(self, id: str) -> dict | None:
        """Gets single event by its ID"""
        with self._get_connection() as con:
            cursor = con.cursor()
            cursor.execute(f"SELECT data FROM {self.table_name} WHERE uuid = ?", (id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return json.loads(row[0])
