resource "aws_lambda_function" "security_auto" {
  filename      = "lambda_function.zip"
  function_name = "SecurityAutomationFunction"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "security_fix.lambda_handler"

  runtime = "python3.9"

  # ارفع الـ Timeout هنا لـ 15 ثانية
  timeout = 15

  # إذا كان بلوك الـ vpc_config موجوداً هنا، قم بعمل comment له مؤقتاً (#)
  # vpc_config {
  #   subnet_ids         = [...]
  #   security_group_ids = [...]
  # }
}