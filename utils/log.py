# -*- encoding: utf-8 -*-
# @File     : log
# @Docs     : log for discord

import logging


class ColourFormatter(logging.Formatter):
    """ Use discord.utils _ColourFormatter """

    LEVEL_COLOURS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]

    FORMATS = {
        level: logging.Formatter(
            f'\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s',
            '%Y-%m-%d %H:%M:%S',
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


class Logger:
    __slots__ = ("log", "colour_handler", "file_handler")

    def __init__(self, filename="discord.log", level=logging.INFO) -> None:
        # Get file path
        library, _, _ = __name__.partition('.')
        self.log = logging.getLogger(library)
        # Set log level
        self.log.setLevel(level)
        # Set handlers
        self.colour_handler = logging.StreamHandler()
        self.file_handler = logging.FileHandler(
            filename, encoding="utf-8", mode="a"
        )
        self.colour_handler.setFormatter(ColourFormatter())
        self.log.addHandler(self.colour_handler)
        self.log.addHandler(self.file_handler)

    def close(self) -> None:
        # 关闭处理程序，避免资源泄漏
        self.colour_handler.close()
        self.file_handler.close()

    def __call__(self) -> logging.Logger:
        return self.log
