output "eventbridge_rule_arn" {
  value = aws_cloudwatch_event_rule.etl_schedule.arn
}
