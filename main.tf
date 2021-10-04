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

resource "aws_security_group" "ned_kelly_sg" {
  name        = "ned_kelly_sg"
  description = "Security group for AWS lambda and AWS RDS connection"
  vpc_id      = aws_default_vpc.default.id
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["127.0.0.1/32"]
    self = true
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}



# Database 
variable "db_password" {
  type    = string
}
variable "db_user" {
  type = string
  default = "nedkelly"
}

variable "db_name" {
  type = string
  default = "kellyhouse"
}

resource "aws_db_instance" "db" {
  allocated_storage    = 10
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  name                 = var.db_name
  username             = var.db_user
  password             = var.db_password
  vpc_security_group_ids = [aws_security_group.ned_kelly_sg.id]
  multi_az             = false
  skip_final_snapshot  = true
}


resource "aws_default_subnet" "default_subnet" {
  availability_zone = aws_db_instance.db.availability_zone

  tags = {
    Name = "Default subnet for database"
  }
}
resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
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
  function_name = "ned-kelly-criterion-hello-world"
  publish       = true
  handler       = "app.lambda_handler"
  runtime       = "python3.9"
  filename = data.archive_file.hello_world_source.output_path
  source_code_hash = data.archive_file.hello_world_source.output_base64sha256
  vpc_config {
      subnet_ids = [aws_default_subnet.default_subnet.id]
      security_group_ids = [aws_security_group.ned_kelly_sg.id]
  }
  environment {
    variables = {
      DB_HOST = aws_db_instance.db.address
      DB_USER = var.db_user
      DB_NAME = var.db_name
      DB_PASSWORD = var.db_password
    }
  }
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

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
    role       = aws_iam_role.hello_world_lambda_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

data "archive_file" "hello_world_source" {
  type             = "zip"
  source_dir       = "${path.module}/.aws-sam/build/HelloWorldFunction"
  output_file_mode = "0666"
  output_path      = "${path.module}/lambda.zip"
}


resource "aws_iam_role" "cloudwatch" {
  name = "api_gateway_cloudwatch_global"

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

resource "aws_iam_role_policy" "cloudwatch" {
  name = "default"
  role = aws_iam_role.cloudwatch.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents",
                "logs:GetLogEvents",
                "logs:FilterLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}