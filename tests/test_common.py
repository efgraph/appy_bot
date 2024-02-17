from unittest.mock import AsyncMock
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand
import pytest
from bot.db.base import sessionmaker
from bot.ui_commands import set_ui_commands
from bot.middlewares.db import DbSessionMiddleware
from bot.__main__ import main


@pytest.mark.asyncio
async def test_set_ui_commands():
    bot = AsyncMock()
    commands = [
        BotCommand(command="generate", description="Generate logo with prompts"),
        BotCommand(command="clear", description="Clear generation history"),
        BotCommand(command="howto", description="Describe bot commands"),
        BotCommand(command="rate", description="Rate logo with offset"),
        BotCommand(command="history", description="View generated logo with offset"),
    ]
    await set_ui_commands(bot)
    bot.set_my_commands.assert_called_once_with(commands=commands, scope=BotCommandScopeAllPrivateChats())


@pytest.mark.asyncio
async def test_db_session_middleware():
    handler = AsyncMock(return_value='handler_response')
    middleware = DbSessionMiddleware(session_pool=sessionmaker)

    mock_event = AsyncMock()
    mock_data = {}

    await middleware(handler, mock_event, mock_data)

    handler.assert_called_once()
    assert 'session' in mock_data


@pytest.mark.asyncio
async def test_dispatcher():
    bot = AsyncMock()
    dp = AsyncMock()
    await main(bot, dp)
    dp.update.middleware.assert_called_once()
    dp.start_polling.assert_called_once()
    assert dp.include_router.call_count == 2
