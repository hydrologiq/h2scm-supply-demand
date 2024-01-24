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

variable "scm_api_id" {
  type = string
  description = "The API id of the SCM API"
}

variable "scm_api_region" {
  type = string
  description = "The region of the SCM API"
}

variable "scm_api_stage" {
  type = string
  description = "The stage of the SCM API"
}
