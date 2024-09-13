import logging
from colorlog import ColoredFormatter


def log(module):
    # Create a logger
    logger = logging.getLogger(module)
    logger.setLevel(logging.DEBUG)  # Set logger to the lowest level to capture all logs

    # Create a handler to output logs to the console (StreamHandler)
    handler = logging.StreamHandler()

    # Create the ColoredFormatter
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s -> %(funcName)s %(log_color)s :: %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,',
        },
        secondary_log_colors={},
        style='%'
    )

    # Set the formatter for the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger
