import logging
import logging.config
import os


# This filter demotes certain uvicorn error messages to INFO level to reduce log noise during startup and shutdown.
class UvicornErrorDemoter(logging.Filter):
    _STARTUP_HINTS = (
        "Started server process",
        "Waiting for application startup",
        "Application startup complete",
        "Uvicorn running on",
        "Shutting down",
        "Finished server process",
        "Waiting for application shutdown",
        "Application shutdown complete",
    )

    def filter(self, record: logging.LogRecord) -> bool:
        if record.name in ("uvicorn.error", "uvicorn"):
            record.name = "app"
            msg = record.getMessage()
            if (
                any(h in msg for h in self._STARTUP_HINTS)
                and record.levelno >= logging.WARNING
            ):
                record.levelno = logging.INFO
                record.levelname = "INFO"
                record.exc_info = None
                record.exc_text = None
        return True


def setup_logging():
    log_dir = os.getenv("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")
    level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                # "()" is the factory hook — the value is what gets called to produce the object, not the object itself.
                # It tells logging to build this filter by importing the class and instantiating it
                "uvicorn_error_demoter": {
                    "()": "app.utils.logging_config.UvicornErrorDemoter"
                },
            },
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                    "filters": ["uvicorn_error_demoter"],
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": log_file,
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf-8",
                    "filters": ["uvicorn_error_demoter"],
                },
            },
            "root": {"level": level, "handlers": ["console", "file"]},
            "loggers": {
                "uvicorn.access": {
                    "handlers": ["console", "file"],
                    "level": level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["console", "file"],
                    "level": level,
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["console", "file"],
                    "level": level,
                    "propagate": False,
                },
            },
        }
    )
