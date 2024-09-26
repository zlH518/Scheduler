import logging
import config
from datetime import datetime


class logger:
    __added_empty_line = False

    @staticmethod
    def log(msg):
        if not logger.__added_empty_line:
            logging.basicConfig(
                filename=config.log_file,
                format=config.log_format,
                level=logging.INFO
            )
            logging.info("\n")
            logging.info(datetime.now())
            logger.__added_empty_line = True
        logging.info(msg)
        print(msg)

