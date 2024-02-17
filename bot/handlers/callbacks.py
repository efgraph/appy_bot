import os
from contextlib import suppress
from pathlib import Path

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from bot.common import PromptsCallbackFactory, ScoresCallbackFactory
from bot.db.models import UserPrompt
from bot.keyboards import generate_prompts
from bot.db.crud import get_user_prompt_by_id

router = Router(name="callbacks-router")


@router.callback_query(PromptsCallbackFactory.filter(F.prompt == "Go"))
async def cb_prompt_go(callback: CallbackQuery, session: AsyncSession):
    prompt = await get_user_prompt_by_id(session, callback.message.message_id)
    await callback.message.answer(text=f'Generating logo by prompt: {prompt.prompt}')
    file_dir = f"{Path(__file__).parent.parent.parent}/static"
    file_name = os.listdir(file_dir)[-1]

    image = FSInputFile(f"{file_dir}/{file_name}")

    result = await callback.message.answer_photo(
        photo=image,
        caption="Generated logo"
    )

    prompt.file_id = result.photo[-1].file_id
    await session.commit()
    await session.close()
    return image


@router.callback_query(PromptsCallbackFactory.filter())
async def cb_prompt(callback: CallbackQuery, session: AsyncSession):
    exists = await session.get(UserPrompt, callback.message.message_id) is not None
    if not exists:
        await session.merge(
            UserPrompt(id=callback.message.message_id, user_id=callback.from_user.id, prompt="Design logo for"))
        await session.commit()
    prompt = await get_user_prompt_by_id(session, callback.message.message_id)
    prompt.prompt += f" {callback.data.split(':')[-1]}"

    await session.commit()
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text=f"{prompt.prompt}", reply_markup=generate_prompts())


@router.callback_query(ScoresCallbackFactory.filter())
async def cb_score(callback: CallbackQuery, session: AsyncSession):
    score = callback.data.split(':')[-2]

    prompt = await get_user_prompt_by_id(session, callback.message.message_id)
    prompt.score = score
    await session.commit()
    await callback.message.answer(text='Thank you for the feedback')
