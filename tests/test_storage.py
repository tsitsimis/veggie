"""Tests for the Storage classes"""
import json
import sqlite3
import tempfile
from pathlib import Path
from typing import Any

import pytest
from veggie.storage import SQLiteStorage, Storage


@pytest.fixture
def temp_db_path() -> Any:
    """Creates a temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".sqlite") as temp_file:
        return temp_file.name


@pytest.fixture
def sqlite_storage(temp_db_path: str) -> Storage:
    """Returns an instance of SQLiteStorage with a temporary database."""
    return SQLiteStorage(path=temp_db_path)


def test_store_event_new(sqlite_storage: SQLiteStorage) -> None:
    """Test storing a new event."""
    event = {"uuid": "12345", "name": "task_completed", "sent_timestamp": 1670000000.0, "data": {"result": "success"}}
    sqlite_storage.store_event(event)

    with sqlite3.connect(sqlite_storage.path) as con:
        cursor = con.cursor()
        cursor.execute("SELECT data FROM events WHERE uuid = ?", (event["uuid"],))
        row = cursor.fetchone()
        assert row is not None
        assert json.loads(row[0]) == event


def test_store_event_update(sqlite_storage: SQLiteStorage) -> None:
    """Test updating an existing event."""
    event = {"uuid": "12345", "name": "task_started", "sent_timestamp": 1670000000.0, "data": {"status": "in_progress"}}
    sqlite_storage.store_event(event)

    updated_event = {
        "uuid": "12345",
        "name": "task_completed",
        "sent_timestamp": 1670000001.0,
        "data": {"status": "completed"},
    }
    sqlite_storage.store_event(updated_event)

    with sqlite3.connect(sqlite_storage.path) as con:
        cursor = con.cursor()
        cursor.execute("SELECT data FROM events WHERE uuid = ?", (event["uuid"],))
        row = cursor.fetchone()
        assert row is not None
        assert json.loads(row[0]) == updated_event


def test_get_events(sqlite_storage: SQLiteStorage) -> None:
    """Test retrieving all events."""
    events = [
        {"uuid": "1", "name": "task_1", "sent_timestamp": 1670000000.0, "data": {"result": "success"}},
        {"uuid": "2", "name": "task_2", "sent_timestamp": 1670000001.0, "data": {"result": "failure"}},
    ]
    for event in events:
        sqlite_storage.store_event(event)

    retrieved_events = sqlite_storage.get_events()
    assert len(retrieved_events) == len(events)
    assert retrieved_events[0]["uuid"] == "2"  # Check sorting by sent_timestamp


def test_get_event_by_id(sqlite_storage: SQLiteStorage) -> None:
    """Test retrieving a single event by its UUID."""
    event = {"uuid": "12345", "name": "task_completed", "sent_timestamp": 1670000000.0, "data": {"result": "success"}}
    sqlite_storage.store_event(event)

    retrieved_event = sqlite_storage.get_event_by_id("12345")
    assert retrieved_event == event


def test_get_event_by_id_not_found(sqlite_storage: SQLiteStorage) -> None:
    """Test retrieving a non-existent event by its UUID."""
    retrieved_event = sqlite_storage.get_event_by_id("non_existent_uuid")
    assert retrieved_event is None


def test_database_creation(sqlite_storage: SQLiteStorage) -> None:
    """Test if the database and table are created properly."""
    assert Path(sqlite_storage.path).exists()

    with sqlite3.connect(sqlite_storage.path) as con:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        table = cursor.fetchone()
        assert table is not None


def test_index_creation(sqlite_storage: SQLiteStorage) -> None:
    """Test if the necessary indexes are created."""
    with sqlite3.connect(sqlite_storage.path) as con:
        cursor = con.cursor()
        cursor.execute("PRAGMA index_list(events)")
        indexes = cursor.fetchall()
        index_names = [index[1] for index in indexes]
        assert "idx_name" in index_names
        assert "idx_sent_timestamp" in index_names
