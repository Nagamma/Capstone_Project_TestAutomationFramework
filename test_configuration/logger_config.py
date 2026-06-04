import logging
import os
#Logging to both console and file

def setup_logger(logger_name, log_file):
    logger = logging.getLogger(logger_name)
    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(os.path.join('logs',log_file),mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

    # logging.basicConfig(
    #     filename="./logs/extraction.log",
    #     filemode='a',
    #     format='%(asctime)s - %(levelname)s - %(message)s',
    #     level=logging.INFO,
    # )

