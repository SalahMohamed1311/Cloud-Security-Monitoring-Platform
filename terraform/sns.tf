resource "aws_sns_topic" "security_alerts" {
  name = "security-alerts-topic"
}

# (اختياري) لو حابب تربط إيميلك عشان يوصلك التنبيهات عليه
resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.security_alerts.arn
  protocol  = "email"
  endpoint  = "salahmo.cloudpso@gmail.com"
}