# Introduction

By default, the serverless frameworks configures lambda functions to write logs out to Cloudwatch Logs.

Cloudwatch Logs is an AWS lo service. It gets logs from Lambda functions asynchrously with some delay (seconds or minutes), and stores them within the service itself. From here logs can be shipped out to an S3 bucket, or be further analyzed within the service itself. 

The service is a serverless offering, and requires no configuration to setup. However, you do pay for log storage, and query (via Cloudwatch insights). In order to reduce you log cost, you can setup the `logRetentionInDays` parameter to delete logs once they get too old.

Note: `Cloudwatch Logs` is a service that is distinct from `Cloudwatch` or rather exists withing Cloudwatch. Do not confuse the two to be same thing.

Let's look at how we can configure our Logging within our Lambda Functions...

# The Python Logging module

To setup logging within a Lambda function use the following code snippet:

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main(event, context):
	logger.info("This is an info message")
	logger.warning("This is a warning message")
	logger.debug("This is a debug message")
	logger.error("This is an error message")
```

If you ran the code above, you would get the following logs in cloudwatch logs:

```
10:48:56 START RequestId: 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 Version: $LATEST
10:48:56 [INFO] 2019-11-16T10:48:56.890Z 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 This is an info message
10:48:56 [WARNING] 2019-11-16T10:48:56.890Z 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 This is a warning message
10:48:56 [ERROR] 2019-11-16T10:48:56.890Z 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 This is an error message
10:48:56 END RequestId: 619e95a0-6ce5-41b6-80db-c5b8f54a3ff2 
```

## Exercise 1.0

To test this out, deploy the project in this folder, and then tail the logs from within serverless.

	$ sls deploy
	$ sls invoke -f log_intro
	$ sls logs -f log_intro

* What did the logs show?
* 4 log messages were written out, why did only 3 appear in the logs?

From this exercise we can see how little setup is required to setup logging from lambda functions in Python. 

# How to read the Default log formats

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

But reading flat-lines of text aren't ideal for analysis and consumption. Instead let's try to change the format of the logs to something better, perhaps JSON.

# Configuring Lambda Log Format

In order to over-write the existing log format into something else (e.g JSON), you'll need to modify the log handler that **already** exist. The log handler called root is added during the bootstrap of your function, you have no control over the setting of this handler, you can only change it post-creation.

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

This allows you to change the format from tab-delimited to JSON, but ultimately the message is still plaintext without any ability to create fields int hem. What if you wanted more structure in your logs. i.e. embed JSON objects into the log message? Let's take a look...

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

The format allows for additional fields to our log output, simply by appending a dictionary to the logger calls. Note the `logClass.py` has a get_formatter method that makes this process easier. As an example:

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

And now we'll have a fully figured JSON output...

```json
{"levelname": "INFO",
 "time": "2019-11-16T08:30:10.4Z",
 "aws_request_id": "0ce03c8c-221f-4487-9756-7771276ba73b",
  "message": "9", 
  "module": "log_test", 
  "data": {
  	"invoke_arn": "arn:aws:lambda:ap-southeast-1:820756113164:function:pycon-bare-minimum-dev-log_test", 
  	"value": 1
  }
}
```

But what's the use of structuring our data if we can't read it programmatically? Fortunately, cloudwatch logs allow us to query large amount of log data using a tool called Cloudwatch insights. It basically grants us SQL like query execution on our logs, with each element of our logs being treated as a column in a database (sort of!)

# Cloudwatch insights basics

By default, each cloudwatch log record will have a @message and @timestamp field. Modifying the format of the log output, changes the format of the @message field (it still exist). But if the format is JSON, then cloudwatch automatically provides the ability to query on fields within @message as well.

For now, we can run a very simple, CloudWatch Insights query using the following format:

```
fields @timestamp, message, data.invoke_arn, data.value
| sort @timestamp desc
| filter data.invoke_arn like /arn:aws/ and data.value > '3' and message > '6'
| limit 200
```

To the keen observer, this looks very similar to SQL Select queries, and indeed we get a nearly free log solution without the need for any servers, agents, or even log files. The platform takes care of this for us. For more granular or in-depth logs, you might still need to spin up something like Elasticsearch etc, and more mature organizations, procuring specific cloud logging tools like DataDog or Epsagon might bring tremendous value. But straight out of the box, CloudWatch Logs + CloudWatch insights give our functions a very good log solution for a very low cost. 

So let's see how all of this works.

# Exercise

Run the log_test function

	$ sls invoke -f log_test

This simple function populates logs in JSON format into cloudwatch, and as we learnt into a single `Log Group` called */aws/lambda/pycon-bare-minimum-dev-log_test*. From there you can run the following query on Cloudwatch insights to see the logs:

```
fields @timestamp, message, data.invoke_arn, data.value
| sort @timestamp desc
| filter data.invoke_arn like /arn:aws/ and data.value > '3' and message > '6'
| limit 200
```

You can do this via console, but here we provide a simple Python script to execute the query above for you.	
	
	$ python3 query_logs.py

At the end of the exercise youu would have created some logs (using `log_test`), understood how the function outputted logs to CloudWatch. Outputted them in JSON (instead of line text items), and query them via the CloudWatch Insights.

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
* How can we output CloudWatch logs to an S3 bucket

# Conclusion

# Additional reading

To learn more, the following references are useful:

* [The python context object in Lambda](https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html)
* [Logging JSON in python](https://stackoverflow.com/questions/50233013/aws-lambda-logs-to-one-json-line)
* [Deep Dive into a Lambda](https://www.denialof.services/lambda/)