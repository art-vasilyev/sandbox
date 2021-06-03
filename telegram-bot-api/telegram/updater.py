import logging
import time
from dataclasses import dataclass
from typing import List

from telegram.api import TelegramAPI
from telegram.handlers import Handler


@dataclass
class Updater:
    api: TelegramAPI
    handlers: List[Handler]
    _offset: int = None
    polling_interval = 1
    logger: logging.Logger = logging.getLogger(__name__)

    def poll(self):
        updates = self.api.get_updates(offset=self._offset)

        for update in updates:
            for handler in self.handlers:
                if handler.check_update(update):
                    self.logger.debug("Run handler %s", handler)
                    handler.handle_update(self.api, update)
                    break

            self._offset = update.update_id + 1

    def run(self):
        self.logger.debug("Staring telegram updater...")
        while True:
            time.sleep(self.polling_interval)
            self.poll()
