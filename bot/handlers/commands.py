from aiogram import Router, html
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from sqlalchemy import select, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import UserPrompt
from bot.keyboards import generate_prompts, generate_scores

router = Router(name="commands-router")


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Hi there!'
    )


@router.message(Command('howto'))
async def cmd_start(message: Message):
    await message.answer(
        """I can help you generate and manage logos with these commands
        
/howto - show commands description
/generate - generate logo with prompts
/clear - clear all history of logos generation
/rate - rate logo with offset in an argument
/history - view generated logo with offset in an argument
        """,
        parse_mode=ParseMode.HTML
    )


@router.message(Command("generate"))
async def cmd_generate(message: Message):
    await message.answer("Design logo for", reply_markup=generate_prompts())


@router.message(Command("history"))
async def cmd_history(message: Message, command: CommandObject, session: AsyncSession):
    offset = 0 if not command.args else command.args.split(" ", maxsplit=1)[0]
    db_query = await session.execute(select(UserPrompt).order_by(desc(UserPrompt.created_date)).offset(offset))
    prompt = db_query.scalar()
    if prompt is None:
        await message.answer('No such an old logo')
    else:
        await message.answer_photo(caption=prompt.prompt, photo=prompt.file_id)


@router.message(Command("rate"))
async def cmd_rate(message: Message, command: CommandObject, session: AsyncSession):
    offset = 0 if not command.args else command.args.split(" ", maxsplit=1)[0]
    db_query = await session.execute(select(UserPrompt).order_by(desc(UserPrompt.created_date)).offset(offset))
    prompt = db_query.scalar()
    if prompt is None:
        await message.answer('No such an old logo')
    else:
        await message.answer_photo(photo=prompt.file_id, reply_markup=generate_scores(prompt.id))


@router.message(Command('clear'))
async def cmd_clear(message: Message, session: AsyncSession):
    await session.execute(delete(UserPrompt).where(UserPrompt.user_id == message.from_user.id))
    await session.commit()
    await message.answer('All is clear')

