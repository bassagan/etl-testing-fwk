output "sns_topic_arn" {
  value = aws_sns_topic.etl_notifications.arn
}
