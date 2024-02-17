import pytest
import asyncio
import json
import os
from bot.db.base import sessionmaker, Base
from sqlalchemy.orm import Session
from bot.db.models import UserPrompt


@pytest.fixture(scope='session')
def session():
    async_session = sessionmaker()
    asyncio.run(init_db(async_session))
    return async_session


async def clear_data(session):
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())
    await session.commit()


async def init_user_prompts(async_session: Session):
    BASE = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(BASE, 'data/userprompt.json')
    user_prompts = json.load(open(file_name))

    async with async_session as db:
        async with db.begin():
            db.add_all([UserPrompt(**prompt) for prompt in user_prompts])


async def init_db(db: Session) -> None:
    await init_user_prompts(db)