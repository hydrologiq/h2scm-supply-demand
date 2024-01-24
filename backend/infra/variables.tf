variable "env" {
  type = string
  description = "The name of this env e.g. dev|test|prod"
}

variable "region" {
  type = string
  description = "The region to deploy AWS resources in"
}

variable "cognito_user_pool_arn" {
  type = string
  description = "The ARN of the cognito user pool"
}
