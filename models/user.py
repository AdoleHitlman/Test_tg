from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, select, update
import datetime

DATABASE_URL = "postgresql+asyncpg://postgres:1@127.0.0.1/Test_tg"

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(10), default='alive')
    status_updated_at = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_alive_users(session: AsyncSession):
    result = await session.execute(select(User).where(User.status == 'alive'))
    return result.scalars().all()

async def update_user_status(session: AsyncSession, user_id: int, status: str):
    await session.execute(update(User).where(User.id == user_id).values(
        status=status,
        status_updated_at=datetime.datetime.utcnow()
    ))
    await session.commit()