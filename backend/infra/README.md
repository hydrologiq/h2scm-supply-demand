# Infra

The infrastructure is deployed using terraform in AWS.

## State

The terraform state is stored within a pre-existing state, you will need to setup your own state S3 bucket and DynamoDB table. You can follow [this guide as an example](https://angelo-malatacca83.medium.com/aws-terraform-s3-and-dynamodb-backend-3b28431a76c1).

## AWS Account

An AWS account is required with permissions to create all the relevant resources, below is an example policy JSON which can be attached to the account.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "dynamodb:List*",
        "dynamodb:Get*",
        "dynamodb:Create*",
        "dynamodb:Delete*",
        "dynamodb:Update*",
        "dynamodb:Put*",
      ],
      "Resource": "*"
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "logs:Create*",
        "logs:Delete*",
        "cloudwatch:Put*",
        "cloudwatch:Get*",
        "cloudwatch:Delete*",
        "cloudwatch:List*",
      ],
      "Resource": "*"
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "s3:List*",
        "s3:Get*",
        "s3:Put*",
        "s3:Delete*",
      ],
      "Resource": "*"
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "apigateway:Delete*",
        "apigateway:Get*",
        "apigateway:Patch*",
        "apigateway:Post*",
        "apigateway:Patch*",
      ],
      "Resource": "*"
    }
  ]
}
```

## Variables

You can find a list of variables needed to deploy the infrastructure in `variables.tf`, none of these variables are sensitive and therefore are stored in `prod.tfvars`. These values will not be updated if they change, so please contact [platform@hydrologiq.com](mailto:platform@hydrologiq.com) or fill out the contact form within [Hydrologiq API Platform](https://www.hydrologiq.com/api-platform/).

## Envs

There are two environment variables needed to deploy terraform these are:

`AWS_ACCESS_KEY_ID` - The generated key for the AWS user running the job.

`AWS_SECRET_ACCESS_KEY` - The generated secret access key for the AWS user running the job.
