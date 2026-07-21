resource "aws_cloudwatch_event_rule" "security_events" {
  name        = "capture-aws-security-events"
  description = "Captures critical IAM and Security Group changes"

  event_pattern = jsonencode({
    "source" : ["aws.iam", "aws.ec2"],
    "detail-type" : ["AWS API Call via CloudTrail"],
    "detail" : {
      "eventName" : [
        "CreateUser",
        "CreateAccessKey",
        "AuthorizeSecurityGroupIngress",
        "ModifySecurityGroupRules",
        "DeleteTrail",
        "PutBucketPolicy"
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.security_events.name
  target_id = "SecurityAutomationLambda"
  arn       = aws_lambda_function.security_auto.arn
}

resource "aws_cloudwatch_event_target" "close_sg_target" {
  rule      = aws_cloudwatch_event_rule.security_events.name
  target_id = "CloseOpenSecurityGroupLambda"
  arn       = aws_lambda_function.close_open_sg.arn
}

resource "aws_lambda_permission" "allow_eventbridge_close_sg" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.close_open_sg.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.security_events.arn
}