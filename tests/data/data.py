import uuid

import aiogram
from aiogram.types import PhotoSize

SEND_PHOTO = aiogram.methods.SendPhoto(photo=[
    PhotoSize(file_id=str(uuid.uuid4()),
              file_unique_id="123",
              file_size=1101,
              width=90,
              height=51

              )], chat_id=123)
