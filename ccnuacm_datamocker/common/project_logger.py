import sys
import logging
import logging.config

__all__ = ["get_logger"]
__author__ = "JixiangXiong"


def get_logger() -> logging.Logger:
    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "formatter": {
                "format": "[%(levelname)s] %(asctime)s - %(filename)s:%(lineno)d - %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S]",
            }
        },
        "handlers": {
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "formatter": "formatter",
                "level": "INFO",
                "stream": sys.stdout,
            },
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "formatter",
                "level": "DEBUG",
                "filename": "datamocker.log",
            },
        },
        "loggers": {
            "datamocker": {
                "level": "DEBUG",
                "handlers": ["consoleHandler", "fileHandler"],
                "propagate": True,
            }
        },
    }

    # 配置 Logger
    logging.config.dictConfig(logger_config)

    return logging.getLogger("datamocker")
