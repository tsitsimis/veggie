""" Test celery monitor."""
from unittest.mock import Mock

import pytest
from celery import Celery
from veggie.monitor import CeleryMonitor
from veggie.storage import Storage


@pytest.fixture
def mock_storage() -> Mock:
    """Returns a mocked Storage instance."""
    return Mock(spec=Storage)


@pytest.fixture
def mock_celery_app() -> Mock:
    """Returns a mocked Celery instance."""
    celery_app = Mock(spec=Celery)
    celery_app.conf.broker_url = "redis://localhost:6379/0"
    return celery_app


@pytest.fixture
def celery_monitor(mock_celery_app: Mock, mock_storage: Mock) -> CeleryMonitor:
    """Returns an instance of CeleryMonitor."""
    return CeleryMonitor(mock_celery_app, mock_storage)


def test_process_task_sent(celery_monitor: CeleryMonitor, mock_storage: Mock) -> None:
    """Test processing of 'task-sent' event."""
    event = {"uuid": "123", "timestamp": 1670000000.0, "name": "task_sent"}
    celery_monitor._process_task_sent(event)

    assert "timestamp" not in event
    assert event["sent_timestamp"] == 1670000000.0
    mock_storage.store_event.assert_called_once_with(event)


def test_process_task_received(celery_monitor: CeleryMonitor, mock_storage: Mock) -> None:
    """Test processing of 'task-received' event."""
    event = {"uuid": "123", "timestamp": 1670000000.0, "name": "task_received"}
    celery_monitor._process_task_received(event)

    assert "timestamp" not in event
    assert event["received_timestamp"] == 1670000000.0
    mock_storage.store_event.assert_called_once_with(event)


def test_process_task_started(celery_monitor: CeleryMonitor, mock_storage: Mock) -> None:
    """Test processing of 'task-started' event."""
    event = {"uuid": "123", "timestamp": 1670000000.0, "name": "task_started"}
    celery_monitor._process_task_started(event)

    assert "timestamp" not in event
    assert event["started_timestamp"] == 1670000000.0
    mock_storage.store_event.assert_called_once_with(event)


def test_process_task_succeeded(celery_monitor: CeleryMonitor, mock_storage: Mock) -> None:
    """Test processing of 'task-succeeded' event."""
    event = {"uuid": "123", "timestamp": 1670000000.0, "name": "task_succeeded"}
    celery_monitor._process_task_succeeded(event)

    assert "timestamp" not in event
    assert event["succeeded_timestamp"] == 1670000000.0
    mock_storage.store_event.assert_called_once_with(event)


def test_process_task_failed(celery_monitor: CeleryMonitor, mock_storage: Mock) -> None:
    """Test processing of 'task-failed' event."""
    event = {"uuid": "123", "timestamp": 1670000000.0, "name": "task_failed"}
    celery_monitor._process_task_failed(event)

    assert "timestamp" not in event
    assert event["failed_timestamp"] == 1670000000.0
    mock_storage.store_event.assert_called_once_with(event)
