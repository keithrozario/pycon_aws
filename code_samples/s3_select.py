import boto3
import json

# Get Randomly Generated bucket name from Terraform deploy
ssm_client = boto3.client('ssm')
bucket_name = ssm_client.get_parameter(Name='/pycon/random-bucket')['Parameter']['Value']


# Perform S3 Select onto a single object
client = boto3.client('s3')
response = client.select_object_content(
    Bucket=bucket_name,
    Key='shodan-export.json.gz',
    ExpressionType='SQL',
    InputSerialization={
        'JSON': {
            'Type': 'LINES'
            },
        'CompressionType': 'GZIP'},
    OutputSerialization={
        'JSON': {
            'RecordDelimiter': '\n'
        }},
    Expression="select * from s3object s WHERE s.ip_str = '39.104.78.133'")

result_text =''

# Parse through event response
for event in response['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        if not str(records) == "":
            result_text += records
print(json.loads(result_text))

print('END')



