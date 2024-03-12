data "template_file" "simulation_openapi" {
  template = "${file("${path.module}/../openapi/SupplyDemandAPI.yml")}"


  vars = {
    lambda_api_run_simulation_arn = "${aws_lambda_function.api_run_simulation.arn}"
    aws_region                    = var.region
    lambda_identity_timeout       = 25000
    cognito_user_pool_arn         = var.cognito_user_pool_arn
  }

}

resource "aws_api_gateway_rest_api" "simulation" {
  name = "Simulation REST API"
  body = "${data.template_file.simulation_openapi.rendered}"
}

resource "aws_api_gateway_deployment" "simulation" {
  rest_api_id = aws_api_gateway_rest_api.simulation.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.simulation.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage_v1" {
  deployment_id = aws_api_gateway_deployment.simulation.id
  rest_api_id   = aws_api_gateway_rest_api.simulation.id
  stage_name    = "v1"
}

resource "aws_api_gateway_method_settings" "all" {
  rest_api_id = aws_api_gateway_rest_api.simulation.id
  stage_name  = aws_api_gateway_stage.stage_v1.stage_name
  
  method_path = "*/*"

  settings {
    logging_level   = "INFO"
    metrics_enabled    = true
    data_trace_enabled = true
  }

  depends_on = [ aws_api_gateway_account.supply_demand, aws_iam_role_policy.cloudwatch ]
}

# API Gateway

resource "aws_lambda_permission" "api_run_simulation_lambda" {
  statement_id  = "AllowAPIGatewayInvokeApiRunSimulation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_run_simulation.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the specified API Gateway.
  source_arn = "${aws_api_gateway_rest_api.simulation.execution_arn}/*/*"
}
