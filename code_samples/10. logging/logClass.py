import logging
import json


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
            'data': record.__dict__.get('data', {}),
        }
        return json.dumps(j)


def get_formatter():
    """
    returns:
        formatter: A logging.Formatter object to format the logs

    source: https://stackoverflow.com/questions/50233013/aws-lambda-logs-to-one-json-line
    """

    formatter = FormatterJSON(
        '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n',
        '%Y-%m-%dT%H:%M:%S'
    )

    return formatter
