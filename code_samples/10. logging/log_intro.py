import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event, context):
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.debug("This is a debug message")
    logger.error("This is an error message")

    return "Done"
