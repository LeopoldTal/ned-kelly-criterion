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

# API

resource "aws_api_gateway_rest_api" "api" {
  name = "ned-kelly-criterion"
}

resource "aws_api_gateway_deployment" "sandbox" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.api.body))
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "sandbox" {
  deployment_id = aws_api_gateway_deployment.sandbox.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = "sandbox"
}

# resource "aws_api_gateway_stage" "production" {

# }

resource "aws_api_gateway_usage_plan" "throttletron" {
  # TODO: Make another usage plan for production.
  name = "throttletron"
  description  = "Sandbox Throttling"
  api_stages {
    api_id = aws_api_gateway_rest_api.api.id
    stage  = aws_api_gateway_stage.sandbox.stage_name
  }
  quota_settings {
    limit  = 1000
    period = "DAY"
  }
  throttle_settings {
    burst_limit = 10
    rate_limit  = 10
  }

}

resource "aws_api_gateway_api_key" "sandbox_key" {
  name = "staging_key"
}

resource "aws_api_gateway_usage_plan_key" "sandbox_key" {
  key_id        = aws_api_gateway_api_key.sandbox_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.throttletron.id
}


resource "aws_api_gateway_resource" "hello" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "hello"
}

resource "aws_api_gateway_method" "hello_get" {
  api_key_required = true
  authorization    = "NONE"
  resource_id      = aws_api_gateway_resource.hello.id
  rest_api_id      = aws_api_gateway_rest_api.api.id
  http_method      = "GET"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.hello.id
  http_method             = aws_api_gateway_method.hello_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.hello_world_function.invoke_arn
}


# LAMBDA

resource "aws_lambda_permission" "hello_world_invoke_permission" {
  statement_id  = "AllowMyDemoAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello_world_function.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/*/* part allows invocation from any stage, method and resource path
  # within API Gateway REST API.
  source_arn = "${aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
}


resource "aws_lambda_function" "hello_world_function" {
  role          = aws_iam_role.hello_world_lambda_role.arn
  function_name = "ned-kelly-criterion-HelloWorldFunction-iVTZjEZfroLa"
  publish       = true
  handler       = "app.lambda_handler"
  runtime       = "python3.9"
  filename = data.archive_file.hello_world_source.output_path
  source_code_hash = data.archive_file.hello_world_source.output_base64sha256

}

resource "aws_iam_role" "hello_world_lambda_role" {
  assume_role_policy = <<EOF
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

data "archive_file" "hello_world_source" {
  type             = "zip"
  source_dir       = "${path.module}/.aws-sam/build/HelloWorldFunction"
  output_file_mode = "0666"
  output_path      = "${path.module}/lambda.zip"
}