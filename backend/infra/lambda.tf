resource "aws_lambda_function" "api_run_simulation" {
  function_name = "ApiRunSimulation"
  filename      = "${path.module}/../lambdas/bundle/dist/api_run_simulation.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambdas/bundle/dist/api_run_simulation.zip")

  handler = "api_run_simulation.handler.lambda_handler"
  runtime = "python3.12"
  timeout = 60

  role = aws_iam_role.lambda_api_run_simulation.arn

  layers = ["arn:aws:lambda:eu-west-2:133256977650:layer:AWS-Parameters-and-Secrets-Lambda-Extension:11"]

  environment {
    variables = {
    }
  }
}