#####################################################################
# Create API Gateway
#####################################################################
resource "aws_api_gateway_rest_api" "main" {
  name        = "pycon-api"
  description = "Managed by Terraform"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

#####################################################################
# Create IAM role for API Gateway
#####################################################################
resource "aws_iam_role" "api-gateway" {
  name = "pycon-api-gateway"
  description = "Managed by Terraform"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

#####################################################################
# Create POLICY for API Gateway to access DDB table(s)
#####################################################################
resource "aws_iam_role_policy" "api-gateway" {
  name = "DDBPolicy"
  role = "${aws_iam_role.api-gateway.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": [
        "${aws_dynamodb_table.songs_table.arn}"
      ]
    }
  ]
}
EOF
}


resource "aws_api_gateway_resource" "songs" {
  rest_api_id = "${aws_api_gateway_rest_api.main.id}"
  parent_id = "${aws_api_gateway_rest_api.main.root_resource_id}"
  path_part = "/api/v1/songs"
}

resource "aws_api_gateway_method" "get-song" {
  rest_api_id = "${aws_api_gateway_rest_api.main.id}"
  resource_id = "${aws_api_gateway_resource.songs.id}"
  http_method = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get-region-integration" {
  rest_api_id = "${aws_api_gateway_rest_api.main.id}"
  resource_id = "${aws_api_gateway_resource.songs.id}"
  http_method = "${aws_api_gateway_method.get-song.http_method}"
  type = "AWS"
  integration_http_method = "GET"
  uri = "${aws_dynamodb_table.songs_table.arn}/GetItem"
  credentials = "${aws_iam_role.api-gateway.arn}"
  request_templates {
    "application/json" = <<EOF
{
    "TableName": "${aws_dynamodb_table.songs_table.name}"
}
EOF
  }
}
