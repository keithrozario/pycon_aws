# INTRODUCTION

By default, serverless frameworks configures lambdas to output their logs to Cloudwatch, which is (in almost all cases) very useful.

Cloudwatch is the AWS default logging offering, and captures the logs from Lambda functions asynchrously. i.e. the Logs are written after the function has completed with some delay.

This is usually sufficient, but you would have to consider other solutions if you require to view logs in real-time for running lambda functions.

# The Python Logging module

To fully utilize the logging functionality in python, use the following code snippet:

<code>
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	logger.info("This is a log message")
</code>


# Advanced Logging

According to this [post](https://www.denialof.services/lambda/), the root logger of an AWS Python lambda is configured as below:

<code>
	logging.Formatter.converter = time.gmtime
	logger = logging.getLogger()
	logger_handler = LambdaLoggerHandler()
	logger_handler.setFormatter(logging.Formatter(
	    '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(message)s\n',
	    '%Y-%m-%dT%H:%M:%S'
	))
	logger_handler.addFilter(LambdaLoggerFilter())
	logger.addHandler(logger_handler)

</code>

If this is a format you're comfortable with, then you're in luck -- no action necessary. However, to modify the format of the logs require a slightly more cumbersome approach.

# Configuring Lambda Log Format

In order to over-write the existing log format into something else (e.g JSON), you'll need to modify the log handler that already exist.

<code>
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	logger.handlers[0].setFormatter(logging.Formatter('{"level": "%(levelname)s", "message": "%(message)s", "time": "%(asctime)s", "name": "%(name)s"}', 
														"%Y-%m-%dT%H:%M:%S"))
	logger.info("Hello")														
</code>

THe example above would provide a log message as follows:

{"level": "INFO", "message": "Hello", "time": "2019-11-14T11:28:00", "name": "root"}

# Why log with JSON

There are many advantages in logging in json (as opposed to plain text), but the primary reason is readability. Logs are useful only if they are readable, if a human being is unable to read or analyze the 