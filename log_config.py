import logging
import logging.handlers

logger = logging.getLogger("LGENSOL Support")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("disaster_tracker.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s -%(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
