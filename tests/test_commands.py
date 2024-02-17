from unittest.mock import AsyncMock, ANY

import pytest
from aiogram.enums import ParseMode
from bot.handlers.commands import cmd_generate, cmd_history, cmd_rate, cmd_start, cmd_howto, cmd_clear, how_to

from bot.db.crud import get_user_prompt_with_offset
from tests.conftest import clear_data


@pytest.mark.asyncio
async def test_cmd_start(session):
    message_mock = AsyncMock()
    await cmd_start(message_mock)
    message_mock.answer.assert_called_once_with(text='Hi there!')


@pytest.mark.asyncio
async def test_cmd_howto(session):
    message_mock = AsyncMock()
    await cmd_howto(message_mock)
    message_mock.answer.assert_called_once_with(**{'text': how_to, 'parse_mode': ParseMode.HTML})


@pytest.mark.asyncio
async def test_cmd_generate(session):
    message_mock = AsyncMock()
    await cmd_generate(message_mock)
    message_mock.answer.assert_called_once()


@pytest.mark.asyncio
async def test_cmd_history_with_no_offset(session):
    message_mock = AsyncMock()
    command_mock = AsyncMock()
    command_mock.args = ''
    prompt = await get_user_prompt_with_offset(session, 0)
    await cmd_history(message_mock, command_mock, session)
    message_mock.answer_photo.assert_called_with(**{'caption': prompt.prompt, 'photo': prompt.file_id})


@pytest.mark.asyncio
async def test_cmd_history_with_offset(session):
    message_mock = AsyncMock()
    command_mock = AsyncMock()
    command_mock.args = '1'
    prompt = await get_user_prompt_with_offset(session, 1)
    await cmd_history(message_mock, command_mock, session)
    message_mock.answer_photo.assert_called_with(**{'caption': prompt.prompt, 'photo': prompt.file_id})


@pytest.mark.asyncio
async def test_cmd_rate(session):
    message_mock = AsyncMock()
    command_mock = AsyncMock()
    command_mock.args = ''
    prompt = await get_user_prompt_with_offset(session, 0)
    await cmd_rate(message_mock, command_mock, session)
    message_mock.answer_photo.assert_called_with(**{'photo': prompt.file_id, 'reply_markup': ANY})


@pytest.mark.order(100)
@pytest.mark.asyncio
async def test_cmd_clear(session):
    message_mock = AsyncMock()
    message_mock.from_user.id = 12
    await cmd_clear(message_mock, session)
    message_mock.answer.assert_called_once()
    await clear_data(session)