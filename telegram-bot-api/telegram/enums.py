from dataclasses import dataclass
from enum import Enum


@dataclass
class ParseMode:
    MARKDOWN_V2 = "MarkdownV2"
    HTML = "HTML"
    MARKDOWN = "Markdown"


class ChatType(Enum):
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"
