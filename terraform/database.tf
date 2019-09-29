## DynamoDB Table
resource "aws_dynamodb_table" "dynamodb_table" {

  name = "pycon_dynamodb"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "pk"
  # use . as separator e.g. us-east-1.requests
  range_key = "rk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "rk"
    type = "S"
  }

  ttl {
    attribute_name = "expires_in"
    enabled = true
  }

}

resource "aws_ssm_parameter" "dynamodb_table_name" {
  type  = "String"
  description = "Name of DynamoDB Table"
  name  = "/pycon/dynamodb_table_name"
  value = "${aws_dynamodb_table.dynamodb_table.name}"
  overwrite = true
}

resource "aws_ssm_parameter" "dynamodb_table_arn" {
  type  = "String"
  description = "ARN of DynamoDB Layers Table"
  name  = "/pycon/dynamodb_layers_table_arn"
  value = "${aws_dynamodb_table.dynamodb_table.arn}"
  overwrite = true
}
