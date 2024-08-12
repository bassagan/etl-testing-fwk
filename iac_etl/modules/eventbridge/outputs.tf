output "eventbridge_rule_arn" {
  value = aws_cloudwatch_event_rule.raw_clean_schedule.arn
}
