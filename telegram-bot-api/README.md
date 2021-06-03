# telegram-bot-api
Sample telegram bot API using `requests` and `pydantic`.

Usage example:

```python
import os

from telegram.api import TelegramAPI
from telegram.updater import Updater
from telegram.entity import Update
from telegram.handlers import TextHandler


def text_callback(api: TelegramAPI, update: Update) -> None:
    print(f'Got text: {update.message.text}')
    api.send_message(update.message.chat.id_, "pong")

    
updater = Updater(
    api=TelegramAPI(token=os.getenv('BOT_TOKEN')),
    handlers=[TextHandler(callback=text_callback)],
)
updater.run()
```