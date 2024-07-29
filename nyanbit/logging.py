import logging
import os
from datetime import datetime


class Logger(object):
    _Logger = None

    @staticmethod
    def create_logger():
        Logger._Logger = logging.getLogger('nyanbit')
        Logger._Logger.setLevel(logging.INFO)
        os.makedirs('./logs', exist_ok=True)

        formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s|%(filename)s-%(funcName)s:%(lineno)s] >> %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        file_handler = logging.FileHandler(
            './logs/' + datetime.now().strftime('%Y%m%d') + '.log', encoding='utf8')
        file_handler.setFormatter(formatter)

        Logger._Logger.addHandler(stream_handler)
        Logger._Logger.addHandler(file_handler)

    @classmethod
    def get_logger(cls):
        return cls._Logger
