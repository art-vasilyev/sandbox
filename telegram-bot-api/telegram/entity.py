from typing import Optional

from pydantic import BaseModel, Field

from telegram.enums import ChatType


class User(BaseModel):
    id_: int = Field(alias="id")
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]


class Chat(BaseModel):
    id_: int = Field(alias="id")
    type: ChatType
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    description: Optional[str]


class Message(BaseModel):
    message_id: int
    from_: Optional[User] = Field(alias="from")
    date: int
    chat: Chat
    forward_from: Optional[User]
    forward_from_chat: Optional[Chat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    forward_date: Optional[int]
    reply_to_message: Optional["Message"]
    via_bot: Optional[User]
    edit_date: Optional[int]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    text: Optional[str]


Message.update_forward_refs()


class Update(BaseModel):
    update_id: int
    message: Optional[Message]
