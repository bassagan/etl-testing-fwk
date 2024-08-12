resource "aws_cloudwatch_event_rule" "raw_clean_schedule" {
  name                = "etl-schedule-${var.env}"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "raw-clean-target" {
  rule      = aws_cloudwatch_event_rule.raw_clean_schedule.name
  target_id = "lambda-target"
  arn       = var.raw_clean_function_arn  # Ensure this is passed correctly from the module

  depends_on = [
    aws_lambda_permission.allow_eventbridge,
  ]
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge-${var.env}-raw-clean"
  action        = "lambda:InvokeFunction"
  function_name = var.raw_clean_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.raw_clean_schedule.arn
  depends_on    = [var.raw_clean_function_name]
}


resource "aws_cloudwatch_event_rule" "clean_curated_schedule" {
  name                = "clean-curated-schedule-${var.env}"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "clean-curated-target" {
  rule      = aws_cloudwatch_event_rule.clean_curated_schedule.name
  target_id = "lambda-target"
  arn       = var.clean_curated_function_arn  # Ensure this is passed correctly from the module

  depends_on = [
    aws_lambda_permission.clean_curated_allow_eventbridge,
  ]
}

resource "aws_lambda_permission" "clean_curated_allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge-${var.env}-clean-curated"
  action        = "lambda:InvokeFunction"
  function_name = var.clean_curated_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.clean_curated_schedule.arn
  depends_on    = [var.clean_curated_function_name]
}
