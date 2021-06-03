import logging
from dataclasses import dataclass
from functools import wraps
from typing import Callable, List

from telegram.api import TelegramAPI
from telegram.entity import Update

LOG = logging.getLogger(__name__)


@dataclass
class Handler:
    callback: Callable[[TelegramAPI, Update], None]

    def check_update(self, update: Update) -> bool:
        raise NotImplementedError

    def handle_update(self, api: TelegramAPI, update: Update) -> None:
        self.callback(api, update)


@dataclass
class TextHandler(Handler):
    def check_update(self, update: Update) -> bool:
        return bool(getattr(update.message, "text", None))


@dataclass
class CommandHandler(Handler):
    command: str

    def check_update(self, update: Update) -> bool:
        text = getattr(update.message, "text", None)
        return (
            text
            and text.startswith("/")
            and text.lstrip("/").split(maxsplit=1)[0] == self.command
        )


def restricted(func: Callable[[TelegramAPI, Update], None], user_ids: List[int]):
    @wraps(func)
    def wrapped(bot: TelegramAPI, update: Update):
        user = update.message.from_
        if user.id_ not in user_ids:
            LOG.warning("Unauthorized user: %s", user)
            return None
        return func(bot, update)

    return wrapped
