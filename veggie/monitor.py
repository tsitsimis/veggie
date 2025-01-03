"""
Celery monitor
"""
import asyncio
import os

from celery import Celery
from celery.events import EventReceiver
from kombu import Connection
from loguru import logger

from .storage import Storage
from .webapp.flask_app import get_flask_app


class CeleryMonitor:
    """
    Celery monitor class
    """

    def __init__(self, celery_app: Celery, storage: Storage) -> None:
        """
        Initializes the monitor
        """
        self.celery_app = celery_app
        self.storage = storage

        self.flask_app = get_flask_app(storage=storage, celery_app=celery_app)

    def _process_task_sent(self, event: dict) -> None:
        event["sent_timestamp"] = event["timestamp"]
        event.pop("timestamp")
        self.storage.store_event(event)

    def _process_task_received(self, event: dict) -> None:
        event["received_timestamp"] = event["timestamp"]
        event.pop("timestamp")
        self.storage.store_event(event)

    def _process_task_started(self, event: dict) -> None:
        event["started_timestamp"] = event["timestamp"]
        event.pop("timestamp")
        self.storage.store_event(event)

    def _process_task_succeeded(self, event: dict) -> None:
        event["succeeded_timestamp"] = event["timestamp"]
        event.pop("timestamp")
        self.storage.store_event(event)

    def _process_task_failed(self, event: dict) -> None:
        event["failed_timestamp"] = event["timestamp"]
        event.pop("timestamp")
        self.storage.store_event(event)

    async def start_event_receiver(self) -> None:
        """Starts the event receiver"""

        def _run_receiver() -> None:
            broker_url = self.celery_app.conf.broker_url
            with Connection(broker_url) as con:
                receiver = EventReceiver(
                    con,
                    handlers={
                        "task-sent": self._process_task_sent,
                        "task-received": self._process_task_received,
                        "task-started": self._process_task_started,
                        "task-succeeded": self._process_task_succeeded,
                        "task-failed": self._process_task_failed,
                    },
                )
                receiver.capture(limit=None, timeout=None)

        await asyncio.to_thread(_run_receiver)

    async def start_webapp(self) -> None:
        """Starts the webapp asynchronously"""

        def _run_webapp() -> None:
            """Starts the UI asynchronously"""
            self.flask_app.run(host="0.0.0.0", port=os.getenv("VEGGIE_PORT", 5000))

        await asyncio.to_thread(_run_webapp)

    def start(self) -> None:
        """Starts all services in the event loop"""

        async def _start_coroutine() -> None:
            event_receiver_task = asyncio.create_task(self.start_event_receiver())
            logger.info("Started Event Receiver")

            webapp_task = asyncio.create_task(self.start_webapp())
            logger.info("Started Web App")

            await asyncio.gather(event_receiver_task, webapp_task)

        asyncio.run(_start_coroutine())
