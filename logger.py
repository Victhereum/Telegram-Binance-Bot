import logging

# custom logger
logger = logging.getLogger(__name__)

# handler
handler = logging.StreamHandler()
logger.setLevel(logging.DEBUG)


# formatter
formatter = logging.Formatter("%(asctime)s : %(message)s")
handler.setFormatter(formatter)

# add handler
logger.addHandler(handler)

