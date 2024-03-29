from pydantic import BaseSettings, SecretStr, PostgresDsn


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: PostgresDsn
    api_logo: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
