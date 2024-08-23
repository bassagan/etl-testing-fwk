resource "aws_sns_topic" "etl_notifications" {
  name = "etl-notifications-${var.env}"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.etl_notifications.arn
  protocol  = "email"
  endpoint  = var.notification_email
}
