from dataclasses import InitVar, dataclass, field
from typing import List, Optional, Union

from pydantic import parse_obj_as
from requests import Session

from telegram.entity import Message, Update
from telegram.enums import ParseMode
from telegram.exceptions import TelegramError


@dataclass
class TelegramAPI:
    token: InitVar[str]
    session: Session = field(default_factory=Session)
    base_url: str = None

    def __post_init__(self, token):
        self.base_url = f"https://api.telegram.org/bot{token}"

    def get_updates(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> List[Update]:
        url = f"{self.base_url}/getUpdates"

        params = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if timeout is not None:
            params["timeout"] = timeout

        response = self.session.get(url, params=params).json()

        if not response["ok"]:
            raise TelegramError(
                code=response["error_code"], description=response["description"]
            )

        return parse_obj_as(List[Update], response["result"])

    def send_message(
        self,
        chat_id: Union[str, int],
        text: str,
        parse_mode: Optional[ParseMode] = None,
        disable_notification=False,
    ) -> Message:
        url = f"{self.base_url}/sendMessage"
        body = {
            "chat_id": chat_id,
            "text": text,
            "disable_notification": disable_notification,
        }
        if parse_mode:
            body["parse_mode"] = parse_mode
        response = self.session.post(url, json=body).json()

        if not response["ok"]:
            raise TelegramError(
                code=response["error_code"], description=response["description"]
            )

        return parse_obj_as(Message, response["result"])
