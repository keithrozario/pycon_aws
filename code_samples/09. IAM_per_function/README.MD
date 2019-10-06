# Code Samples

This sample demonstrates the ability to specify an IAM per function using the `serverless-iam-roles-per-function` serverless plugin.

The `serverless.yml` file describes two functions, one with an IAM role that can read the bucket and one that can't.

By default, serverless createa an basic execution IAM role for the function, with the ability to write into cloudwatch and creates cloudwatch logstreams. Additional IAM roles can be specified but only at the service level (all functions in the service share the same IAM permssions)

The plugin allows for IAM roles to be specified per function,allowing for better security, since a compromised function would still have limited scope in it's ability to access the Account resources.

# Pre-requisites

* [Terraform](https://terraform.io/)
* [Serverless Framework](https://serverless.com/)

# Other notes

WIP    
 