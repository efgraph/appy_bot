from sqlalchemy.orm import declarative_base

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config_reader import config


Base = declarative_base()

engine = create_async_engine(url=config.db_url, echo=True)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
