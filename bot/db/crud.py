

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from bot.db import UserPrompt


async def get_user_prompt_by_id(session: AsyncSession, message_id: int) -> UserPrompt:
    db_query = await session.execute(select(UserPrompt).filter_by(id=message_id))
    prompt: UserPrompt = db_query.scalar()
    return prompt


async def get_user_prompt_with_offset(session: AsyncSession, offset: int) -> UserPrompt:
    db_query = await session.execute(select(UserPrompt).order_by(desc(UserPrompt.created_date)).offset(offset))
    prompt = db_query.scalar()
    return prompt
