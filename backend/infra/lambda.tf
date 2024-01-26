resource "aws_lambda_function" "api_run_simulation" {
  function_name = "ApiRunSimulation"
  filename      = "${path.module}/../lambdas/bundle/dist/api_run_simulation.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambdas/bundle/dist/api_run_simulation.zip")

  handler = "api_run_simulation.handler.lambda_handler"
  runtime = "python3.12"
  timeout = 60

  role = aws_iam_role.lambda_api_run_simulation.arn

  layers = [aws_lambda_layer_version.simulation.arn]

  environment {
    variables = {
      SCM_API_ID = var.scm_api_id
      SCM_API_REGION = var.scm_api_region
      SCM_API_STAGE = var.scm_api_stage
    }
  }
}