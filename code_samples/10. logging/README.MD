# Introduction

By default, serverless frameworks configures lambda functions to output logs to Cloudwatch Logs.

Cloudwatch Logs is the AWS default logging service. It captures the logs from Lambda functions asynchrously i.e. the Logs are written **after** the function has completed with some delay (seconds or minutes), and stores them within the service itself.

Cloudwatch Logs is a fully serverless offering, and requires no configuration to setup. However, you do pay for log storage, and query (via Cloudwatch insights). In order to reduce you log cost, you can setup the `logRetentionInDays` parameter to delete logs once they get too old.

Let's look at how we can configure our Logging within our Lambda Functions...

# The Python Logging module

To setup logging within a Lambda function use the following code snippet:

```python
logger = logging.getLogger()
logger.setLevel(logging.INFO)
```

after that, from within the function code, we can log out messages using python's built-in logging mechanism

```python
def main(event, context):
	logger.info("This is an info message")
	logger.warning("This is a warning message")
	logger.debug("This is a debug message")
	logger.error("This is an error message")
```

If you ran the code above, you would get the following logs in cloudwatch logs:

10:48:56 START RequestId: 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 Version: $LATEST
10:48:56 [INFO] 2019-11-16T10:48:56.890Z 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 This is an info message
10:48:56 [WARNING] 2019-11-16T10:48:56.890Z 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 This is a warning message
10:48:56 [ERROR] 2019-11-16T10:48:56.890Z 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 This is an error message
10:48:56 END RequestId: 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 

Question: Why didn't the debug message appear on the logs?

Let's now look at making these logs more effective for reading...

# Log Formats

The standard log format is tab delimited text made up of the following four fields.

* Level
* Time(isoformat).milliseconds
* AWS_REQUEST_ID
* Log Message

```python
logger_handler.setFormatter(logging.Formatter(
    '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(message)s\n',
    '%Y-%m-%dT%H:%M:%S'
))
```

This [post](https://www.denialof.services/lambda/) goes into the details of the lambda function where the the root logger is configured as above. 

But what if you wanted to change the log format? Logging as tab delimited fields is better than not logging, but most of your existing tooling might require JSON. Let's see if we can change out logs from tab-delimited to JSON.

# Configuring Lambda Log Format

In order to over-write the existing log format into something else (e.g JSON), you'll need to modify the log handler that **already** exist, or remove the existing log handler and add your own. The root handler is added during the bootstrap time of your function, you have no control over the setting of this handler, you can only change it or delete it.

To change the format of our logs, we'll change the existing handler using the code below:

```python
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers[0].setFormatter(logging.Formatter('{"level": "%(levelname)s", "message": "%(message)s", "time": "%(asctime)s", "name": "%(name)s"}', 
													"%Y-%m-%dT%H:%M:%S"))
logger.info("Hello")														
```

The example above would provide a log message as follows:

```json

{"level": "INFO", "message": "Hello", "time": "2019-11-14T11:28:00", "name": "root"}

```

This allows you to change the log to JSON format, but ultimate the message element is still plaintext. What if you wanted more structure in your logs. i.e. embed JSON objects into the log themselves.

# Configuring Lambda Log Format (next step)

To create a more structured log format out of our functions, we'll need to modify Log format. For that we'll now create class to handle this.

```python
class FormatterJSON(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        j = {
            'levelname': record.levelname,
            'time': '%(asctime)s.%(msecs)dZ' % dict(asctime=record.asctime, msecs=record.msecs),
            'aws_request_id': getattr(record, 'aws_request_id', '00000000-0000-0000-0000-000000000000'),
            'message': record.message,
            'module': record.module,
            'extra_data': record.__dict__.get('data', {}),
        }
        return json.dumps(j)
```

and then use this format. The format allows for additional fields to our log output, simply by appending a dictionary to the logger calls. Note the `logClass.py` has a get_formatter method that makes this process easier.

```python
from logClass import get_formatter
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers[0].setFormatter(get_formatter())

def main(event, context):
	extra = {'data': {'invoke_arn': context.invoked_function_arn,
					  'value': 'random'}} 
	time.sleep()
	logger.info('Hello', extra=extra)

```
Note: you must put all the additional data you want to log in the `data` element of your extra dictionary for this to work.

# CloudWatch Streams and Logs

By default, serverless framework provisions a Cloudwatch `Log Group` for each individual lambda function. Every execution of that function writes out logs to a specific `Log Group`.

Within each `Log Group` are `Log Streams` -- which are more granular partitions of the logs. Under the hood each log stream belongs to a single execution context, with every invocation on a specific execution context written to the same `Log Stream`. 

In short, the relationship:

* Every function has one Log Group
* All logs from this function will go to that Log Group
* Every execution context writes to a Log Stream
* Every Log Group will have many Log Streams

# Why log with JSON

There are many advantages in logging in json (as opposed to plain text), but the primary reason is readability. Logs are useful only if they are readable by actual human beings.

Cloudwatch provides a feature called Cloudwatch insights, which provides SQL-like query abilities on Cloudwatch logs. If you use the default log format in lambda, it's hard to parse through a flat-line of text. But if you log out in json, Cloudwatch insights allow for you to query on fields in those logs.

# Cloudwatch insights basics

By default, each cloudwatch log record will have a @message and @timestamp field. Modifying the format of the log output, changes the format of the @message field (it still exist). But if the format is JSON, then cloudwatch automatically provides the ability to query on fields within @message as well.

# Exercise

Deploy the project in this folder, and run the log_test function

	$ sls deploy
	$ sls invoke -f log_test

The simple log_test function populates logs in JSON format into cloudwatch, and as we learnt into a single `Log Group` called */aws/lambda/pycon-bare-minimum-dev-log_test*. From there you can run the following query on Cloudwatch insights to see the logs:

	$ python3 query_logs.py

```
fields @timestamp, message, data.invoke_arn, data.value
| sort @timestamp desc
| filter data.invoke_arn like /arn:aws/ and data.value > '3' and message > '6'
| limit 200
```

A programmatic example is demonstrated by the `log_test.py` file in this repository.

# Test your understanding

* Are cloudwatch logs recorded in real-time or with a delay?
* What is the standard format of Cloudwatch logs from Python lambda functions?
* How do we modify the format of the logs?
* What is the difference between Log Groups and Log Streams?
* Will the logs from two functions end up in the same Log Group?
* If we use the standard log format, can we still perform Cloudwatch insights Query on them?
* Could we query the output of multiple functions using cloudwatch insights? (answer is yes -- figure out how!)

# Advanced questions

* Are there IAM permissions required to write out to Cloudwatch?
* Modify the query in the exercise to check for fields where data.value is greater than 5
* Modify query_logs.py to search for all logs from the last 2 minutes only (hint: it's not in the query itself)
* Modify query_logs.py to list out only error logs (those logged with logger.error)

# Conclusion

# Additional reading

To learn more, the following references are useful:

* [The python context object in Lambda](https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html)
* [Logging JSON in python](https://stackoverflow.com/questions/50233013/aws-lambda-logs-to-one-json-line)
* [Deep Dive into a Lambda](https://www.denialof.services/lambda/)