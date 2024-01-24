# Deployment

## CircleCI

We use the following context `scm-sd-infra-<env>`

### Storing a secret

Run the below command and then enter the secret value

`circleci context store-secret github hydrologiq scm-sd-infra-<env> <SECRET_NAME>`

### Lambda secrets

`GITHUB_PERSONAL_TOKEN` - The token used for fetching the ontology.

## Terraform deployment

The user to use for this is generated via the aws terraform with limited permissions.

`AWS_ACCESS_KEY_ID` - The generated key for the AWS CI user running the job.

`AWS_SECRET_ACCESS_KEY` - The generated secret access key for the AWS CI user running the job.
