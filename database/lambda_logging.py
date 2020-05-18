import logging


logger = logging.getLogger("ebay_consumer")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
