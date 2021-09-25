terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_api_gateway_rest_api" "api" {
    name =  "ned-kelly-criterion"
}

resource "aws_api_gateway_resource" "hello" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "hello"
}

resource "aws_api_gateway_method" "hello_world" {
    api_key_required = true
    authorization = "NONE"
    resource_id = aws_api_gateway_resource.hello.id
    rest_api_id = aws_api_gateway_rest_api.api.id
    http_method = "GET"
}

resource "aws_api_gateway_integration" "lambda_integration" {
    rest_api_id = aws_api_gateway_rest_api.api.id
    resource_id = aws_api_gateway_resource.hello.id
    http_method = aws_api_gateway_method.hello_world.http_method
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.function.invoke_arn
}

resource "aws_lambda_function" "function" {
    role = aws_iam_role.lambda_role.arn
    function_name = "ned-kelly-criterion-HelloWorldFunction-iVTZjEZfroLa"
    publish = true
    handler = "app.lambda_handler"
    runtime = "python3.9"
}

resource "aws_iam_role" "lambda_role"{
    assume_role_policy =  <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}