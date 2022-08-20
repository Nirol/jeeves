import random

from models.user import UserDAL


def _get_random_location():
    return random.choice(["New York", "San Francisco", "Los Angeles", "Seattle", "Austin", "Boston", "Jerusalem"])

async def create_demo_users(users_dal: UserDAL):
    # create demo users
    for id in range(1, 100):
        await users_dal.create_user(
            name="John Doe",
            email="jd@test.com",
            location=_get_random_location(),
        )