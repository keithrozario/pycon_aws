import logging
import json
from logClass import get_formatter

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers[0].setFormatter(get_formatter())

def main(event, context):
	my_input = {'key1': 'value1'}
	logger.info('Process Info: %s', 'Hello', extra=dict(data=my_input))

	return "Done"