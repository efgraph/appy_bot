import pytest
from unittest.mock import AsyncMock, ANY
from bot.handlers.callbacks import cb_prompt_go, cb_prompt, cb_score
from bot.db.crud import get_user_prompt_by_id
from tests.data.data import SEND_PHOTO


@pytest.mark.asyncio
async def test_cb_prompt_go(session):
    callback = AsyncMock()
    callback.message.message_id = 12
    callback.message.answer_photo.return_value = SEND_PHOTO
    prompt = await get_user_prompt_by_id(session, callback.message.message_id)

    image = await cb_prompt_go(callback, session)

    callback.message.answer_photo.assert_called_with(**{'caption': 'Generated logo', 'photo': image})
    callback.message.answer.assert_called_with(text=f'Generating logo by prompt: {prompt.prompt}')
    assert image is not None


@pytest.mark.asyncio
async def test_cb_prompt(session):
    callback = AsyncMock()
    callback.message.message_id = 12
    message_added = 'a food store'
    callback.data = f':{message_added}'

    prompt = await get_user_prompt_by_id(session, callback.message.message_id)
    message_initial = prompt.prompt
    await cb_prompt(callback, session)
    callback.message.edit_text.assert_called_with(
        **{'text': f'{message_initial} {message_added}', 'reply_markup': ANY})


@pytest.mark.asyncio
async def test_cb_score(session):
    callback = AsyncMock()
    callback.message.message_id = 12
    callback.data = ':5:22'
    await cb_score(callback, session)
    prompt = await get_user_prompt_by_id(session, callback.message.message_id)
    assert prompt.score == 5
    callback.message.answer.assert_called_with(text='Thank you for the feedback')