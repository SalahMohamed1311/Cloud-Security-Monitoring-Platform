# --- 1. Archive files for Lambda ---
data "archive_file" "close_sg_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/close-open-security-group"
  output_path = "${path.module}/files/close_open_security_group.zip"
}

data "archive_file" "notify_user_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/notify-new-user"
  output_path = "${path.module}/files/notify_new_user.zip"
}

data "archive_file" "detect_ak_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/detect-access-key"
  output_path = "${path.module}/files/detect_access_key.zip"
}

# --- 2. Lambda Functions ---
resource "aws_lambda_function" "close_open_sg" {
  filename         = data.archive_file.close_sg_zip.output_path
  function_name    = "close-open-security-group"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.close_sg_zip.output_base64sha256
}

resource "aws_lambda_function" "notify_new_user" {
  filename         = data.archive_file.notify_user_zip.output_path
  function_name    = "notify-new-user"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.notify_user_zip.output_base64sha256
  
  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.security_alerts.arn
    }
  }
}

resource "aws_lambda_function" "detect_access_key" {
  filename         = data.archive_file.detect_ak_zip.output_path
  function_name    = "detect-access-key"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.detect_ak_zip.output_base64sha256
  
  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.security_alerts.arn
    }
  }
}