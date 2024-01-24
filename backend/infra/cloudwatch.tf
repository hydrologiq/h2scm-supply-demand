resource "aws_cloudwatch_log_group" "api_run_simulation" {
  name = "/aws/lambda/${aws_lambda_function.api_run_simulation.function_name}"

  retention_in_days = 30
}