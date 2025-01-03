"""Test celery monitor."""
import datetime
import os
from typing import Any, Literal

from celery import Celery

celery_app = Celery("tasks", broker=os.environ["CELERY_BROKER_URL"], backend=os.environ["CELERY_RESULT_BACKEND"])
celery_app.conf.timezone = "UTC"
celery_app.conf.worker_send_task_events = True
celery_app.conf.task_send_sent_event = True
celery_app.conf.task_track_started = True
celery_app.conf.result_extended = True


@celery_app.task(name="run_model", bind=True)
def run_model(self: Any, model_name: str) -> dict:
    """Run model"""
    return {"prediction": 0.85, "model_name": model_name}


@celery_app.task(name="add_one")
def add_one(my_number: int, when: datetime.datetime, flag: bool, name: str = "bar") -> int:
    """Adds one"""
    import time

    time.sleep(10)
    return my_number + 1


@celery_app.task(name="foo")
def foo(obj: dict, options: Literal["foo", "bar"]) -> dict:
    """Foo"""
    return obj
