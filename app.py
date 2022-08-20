from contextlib import asynccontextmanager

from quart import Quart
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Initialize SQLAlchemy with a test database
from models.user import UserDAL, Base
from utils.create_demo_users import create_demo_users

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



#
# Quart App
#
app = Quart(__name__)


@app.before_serving
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with user_dal() as bd:
            await create_demo_users(bd)



@asynccontextmanager
async def user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)


@app.post("/users")
async def create_user(name, email):
    async with user_dal() as ud:
        await ud.create_user(name, email)


@app.get("/users/<int:user_id>")
async def get_user(user_id):
    async with user_dal() as ud:
        return await ud.get_user(user_id)


@app.get("/users")
async def get_all_users():
    async with user_dal() as ud:
        users_list: list =  await ud.get_all_users()
        return {"users": users_list}


@app.get("/")
async def hello_world():
    return "hello world!"


if __name__ == "__main__":
    app.run()