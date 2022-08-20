# weather_worker.py


from asgiref.sync import async_to_sync

from app import user_dal
from celery import Celery

from models.user import User

celery_app = Celery("tasks", broker="amqp://localhost")


async def fetch_weather(location):
    return "This is where we would call the weather service"


async def send_message_to_user(message, name):
    print(f"user:{name} post message: {message}")


async def weather_alerts_async():
    async with user_dal() as ud:
        query_results: list = await ud.get_all_users()
        for user in query_results:
            user: User = user[0]  # the database returns a tuple
            weather_message = await fetch_weather(user.location)

            await send_message_to_user(message=weather_message, name=user.name)


@celery_app.task
def do_weather_alerts():
    async_to_sync(weather_alerts_async)()

