# Intro to Serverless - 5minutes

Use the slide from serverless meetup...

# Quick API demo - 5 minutes

[bare_minimum](code_samples/01. bare_minimum)

Let the platform do the work...

### End Code
∂
    $ sls deploy
    $ sls invoke -f hello

# Using memory - 3 minutes

One of the downsides of using Lambda functions is that everything goes in/out of it via the network interface..

One trick is to use in-memory programming rather than disk to handle it

    $ sls invoke -f copy
    $ sls invoke -f copy -d "{\"key\": \"100.txt\"}"
    $ sls invoke -f copy_big -d "{\"key\": \"1024.txt\", \"iter\": 1, \"using\": \"memory\"}"
    $ sls invoke -f copy -d "{\"key\": \"100.txt\", \"iter\": 5, \"using\": \"memory\"}"
    $ sls invoke -f copy -d "{\"key\": \"100.txt\", \"iter\": 5, \"using\": \"disk\"}"

# Using S3 Select & Athena - 2 minute

Don't miss a trick though -- if you're intending to process JSON or CSV files, use [S3 select](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectSELECTContent.html) instead. Doing it in the Lambda is attractive, but S3 Select is far more efficient

S3 select has a limit on file sizes, and record sizes in S3 though .. so be careful.

For more complex queries, especially across multiple files -- AWS Athena is awesome. But be careful, it's not available in all AWS Regions.

# Lambda Lifecycle - 5 minutes

Lambda has an odd lifecycle, that usually involves complicated jargon like execution context etc etc.

Slide with butterfly, egg and execution

# To reduce execution time - 2 minute

Move all non-event based code outside the handler ... 

# To reduce Load time... -  2 minute

Reduce size of the package...

Using Layers...

# Using Layers in your Lambda Functions - 5 minutes

Example of a layer straight from code

# Using Public Layers - 3 minutes

# Lambci /Docker lambda - 2 minutes

# Multi-threading in Lambda - 3 minutes

# Lambda@Edge

# Optional
### SSM variables between Terraform and Serverless
### Environment Variables in Serverless
### Amazon xray for customization
### Step Functions
 
# End