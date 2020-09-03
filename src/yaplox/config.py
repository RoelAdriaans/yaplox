import logging

import structlog
from classyconf import Configuration, EnvFile, Environment, EnvPrefix, Value, as_boolean


class AppConfig(Configuration):
    """Configuration for Yaplox"""

    class Meta:
        loaders = [
            Environment(keyfmt=EnvPrefix("YAPLOX_")),
            EnvFile(".env"),
        ]

    DEBUG = Value(default=False, cast=as_boolean, help="Toggle debugging mode.")


def set_logging():
    if config.DEBUG:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    structlog.configure(
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


config = AppConfig()
set_logging()
