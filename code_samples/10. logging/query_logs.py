import boto3
import time

client = boto3.client('logs')

# query, identical to what is found in README.MD
query = '''
fields @timestamp, message, data.invoke_arn, data.value
| sort @timestamp desc
| filter data.invoke_arn like /arn:aws/ and data.value > '3' and message > '6'
| limit 200
'''

# Start the query
response = client.start_query(
    logGroupNames=['/aws/lambda/pycon-bare-minimum-dev-log_test'],
    startTime=int(time.time()) - 3600,
    endTime=int(time.time()),
    queryString=query,
    limit=100
)

query_id = response['queryId']

# Check if query is complete -- this code is bad, don't follow it!
while True:
    response = client.get_query_results(queryId=query_id)
    if response['status'] in ['Complete', 'Failed', 'Cancelled']:
        break
    else:
        pass

# print results
for result in response['results']:
    print(result)


