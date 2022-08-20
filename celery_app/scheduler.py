# weather_worker.py

from celery import Celery
from celery_app.worker import do_weather_alerts

celery_app = Celery("tasks", broker="amqp://localhost")


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, do_weather_alerts, name="add every 10", expires=30)