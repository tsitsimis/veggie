"""Veggie monitor"""
from veggie.monitor import CeleryMonitor
from veggie.storage import SQLiteStorage

from example.tasks import celery_app

if __name__ == "__main__":
    celery_monitor = CeleryMonitor(celery_app=celery_app, storage=SQLiteStorage(path="events.db"))
    celery_monitor.start()
