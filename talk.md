+ serverless create --template aws-python


### Cleanup Yaml


    service: pycon
    
    provider:
      name: aws
      region: ap-southeast-1
      runtime: python3.7
    
    functions:
      hello:
        handler: handler.hello
        memorySize: 128
        timeout: 30
        events:
          - http:
              path: /api/v1/hello
              method: GET
    
    package:
     exclude:
       - venv/**

###

### Cleanup Code


    import json
    
    
    def hello(event, context):
        body = {
            "message": "Go Python"
        }
    
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    
        return response

### End Code

+ sls deploy
+ sls invoke -f hello
+ curl the API endpoint

# Using memory

sls invoke -f copy
sls invoke -f copy -d "{\"key\": \"100.txt\"}"
sls invoke -f copy_big -d "{\"key\": \"1024.txt\", \"iter\": 1, \"using\": \"memory\"}"

# Using S3 Select & Athena

Don't miss a trick though -- if you're intending to process JSON or CSV files, use [S3 select](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectSELECTContent.html) instead. Doing it in the Lambda is attractive, but S3 Select is far more efficient

S3 select has a limit on file sizes, and record sizes in S3 though .. so be careful.

For more complex queries, especially across multiple files -- AWS Athena is awesome. But be careful, it's not available in all AWS Regions.

# 