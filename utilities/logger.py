import os
import logging
from logging.handlers import TimedRotatingFileHandler

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

class LoggerManager:
    """
    Logger singleton class.
    """
    # Here will be the instance stored.
    __logger = None

    @staticmethod
    def get_logger():
        """ Static access method. """
        if LoggerManager.__logger == None:
            LoggerManager()
        return LoggerManager.__logger

    def __init__(self):
        if LoggerManager.__logger != None:
            raise Exception("This class is a singleton!")
        else:
            handler = TimedRotatingFileHandler(BASE_PATH + '/logs/probot.log',
                                               when="w0",
                                               interval=1,
                                               backupCount=5)
            handler.setFormatter(logging.Formatter(
              '[%(asctime)s [%(levelname)s | %(filename)s:%(lineno)s]] :: %(message)s'))
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            LoggerManager.__logger = logger
