import logging
from pathlib import Path

def get_logger(name: str, level: int = logging.DEBUG, out=None) -> logging.Logger:
    logger = logging.getLogger(name.split('.')[-1])
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    if out:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        out_handler = logging.FileHandler(log_dir.joinpath(out))
    else:
        out_handler = logging.StreamHandler()
    out_handler.setFormatter(formatter)
    logger.addHandler(out_handler)
    return logger
