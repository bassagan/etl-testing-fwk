resource "aws_cloudwatch_event_rule" "etl_schedule" {
  name                = "etl-schedule-${var.env}"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "etl_target" {
  rule      = aws_cloudwatch_event_rule.etl_schedule.name
  target_id = "lambda-target"

  arn = var.lambda_function_arn  # Ensure this is passed correctly from the module

  depends_on = [
    aws_lambda_permission.allow_eventbridge,
  ]
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.etl_schedule.arn
  depends_on = [var.lambda_function_name]

}
