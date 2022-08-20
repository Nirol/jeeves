# user model
from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Data Model



class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    location = Column(String)
    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "location": self.location,

        }


# Data Access Layer
class UserDAL:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_user(
        self,
        name,
        email,
        location,

    ):
        new_user = User(
            name=name,
            email=email,
            location=location,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user.json()





    async def get_all_users(self) -> list:
        query_result = await self.db_session.execute(select(User).order_by(User.id))
        return [user.json() for user in query_result.scalars().all()]

    async def get_user(self, user_id):
        query = select(User).where(User.id == user_id)
        query_result = await self.db_session.execute(query)
        user = query_result.one()
        return user[0].json()
