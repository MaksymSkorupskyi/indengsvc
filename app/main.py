import logging
import os

from app.routes import api_app

app = api_app
logger = None


def setup_logging(level=logging.INFO):
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    filename = '{}.log'.format(os.path.splitext(os.path.basename(__file__))[0])
    ch = logging.FileHandler(filename)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return filename


setup_logging()
