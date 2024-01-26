resource "aws_lambda_layer_version" "simulation" {
  filename   = "${path.module}/../lambdas/bundle/dist_layers/simulation.zip"
  layer_name = "simulation"
  source_code_hash = filebase64sha256("${path.module}/../lambdas/bundle/dist_layers/simulation.zip")

  compatible_runtimes = ["python3.12"]
}