from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import UserPrompt
from bot.keyboards import generate_prompts, generate_scores
from bot.db.crud import get_user_prompt_with_offset

router = Router(name="commands-router")

how_to = """I can help you generate and manage logos with these commands
        
/howto - show commands description
/generate - generate logo with prompts
/clear - clear all history of logos generation
/rate - rate logo with offset in an argument
/history - view generated logo with offset in an argument
        """


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text='Hi there!')


@router.message(Command('howto'))
async def cmd_howto(message: Message):
    await message.answer(text=how_to, parse_mode=ParseMode.HTML)


@router.message(Command("generate"))
async def cmd_generate(message: Message):
    await message.answer("Design logo for", reply_markup=generate_prompts())


@router.message(Command("history"))
async def cmd_history(message: Message, command: CommandObject, session: AsyncSession):
    offset = 0 if not command.args else command.args.split(" ", maxsplit=1)[0]
    prompt = await get_user_prompt_with_offset(session, offset)
    if prompt is None:
        await message.answer('No such an old logo')
    else:
        await message.answer_photo(caption=prompt.prompt, photo=prompt.file_id)


@router.message(Command("rate"))
async def cmd_rate(message: Message, command: CommandObject, session: AsyncSession):
    offset = 0 if not command.args else command.args.split(" ", maxsplit=1)[0]
    prompt = await get_user_prompt_with_offset(session, offset)
    if prompt is None:
        await message.answer('No such an old logo')
    else:
        await message.answer_photo(photo=prompt.file_id, reply_markup=generate_scores(prompt.id))


@router.message(Command('clear'))
async def cmd_clear(message: Message, session: AsyncSession):
    await session.execute(delete(UserPrompt).where(UserPrompt.user_id == message.from_user.id))
    await session.commit()
    await message.answer('All is clear')
