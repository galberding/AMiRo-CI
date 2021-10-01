import logging
from pathlib import Path

DEFAULT_LOG_LEVEL = logging.DEBUG

def get_logger(name: str, level: int = DEFAULT_LOG_LEVEL, out='general.log') -> logging.Logger:
    """!Create custom names logger.
    As default the logger will log to the terminal.
    @param name name of the logger
    @param level log level, leave empty to use the global log level
    @param out name of the log file, if set all nothing is logged to the terminal.

    @note all logs are saved under the current work directory/logs
    """
    logger = logging.getLogger(name.split('.')[-1])
    logger.setLevel(level)
    formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
    if out:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        out_handler = logging.FileHandler(log_dir.joinpath(out))
    else:
        out_handler = logging.StreamHandler()
    out_handler.setFormatter(formatter)
    logger.addHandler(out_handler)
    return logger
