import logging
import random

from logClass import get_formatter
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers[0].setFormatter(get_formatter())


def main(event, context):

	for _ in range (100):
		extra = {'data': {'invoke_arn': context.invoked_function_arn,
				  'value': random.randint(1,5)}}
		logger.info(random.randint(6,10), extra=extra)
		if _ % 10 == 0:
			logger.error("there was an error", extra=extra)

	return "Done"