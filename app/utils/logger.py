# logger.py
from rich.logging import RichHandler
import logging


class CustomLogger:
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.logger.addHandler(RichHandler())

    def get_logger(self):
        return self.logger


logger = CustomLogger().get_logger()
