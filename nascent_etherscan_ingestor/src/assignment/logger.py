import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('thread_errors.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

