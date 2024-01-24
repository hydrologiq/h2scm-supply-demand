terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket         = "scm-sd-terraform-state-backend"
    key            = "terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "scm-sd_terraform_state"
  }
}