output "eventbridge_rule_arn" {
  value = aws_cloudwatch_event_rule.raw_clean_schedule.arn
}
output "clean_curated_eventbridge_rule_arn" {
  description = "ARN of the EventBridge rule for clean-curated schedule"
  value       = aws_cloudwatch_event_rule.clean_curated_schedule.arn
}

output "raw_clean_eventbridge_target_arn" {
  description = "ARN of the EventBridge target for raw-clean schedule"
  value       = aws_cloudwatch_event_target.raw-clean-target.arn
}

output "clean_curated_eventbridge_target_arn" {
  description = "ARN of the EventBridge target for clean-curated schedule"
  value       = aws_cloudwatch_event_target.clean-curated-target.arn
}

