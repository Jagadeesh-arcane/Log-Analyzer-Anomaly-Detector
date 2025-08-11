#!/usr/bin/env bash
set -euo pipefail

AWS_REGION="${AWS_REGION:-us-east-1}"
SHORT_SHA="${CI_COMMIT_SHORT_SHA:-$(git rev-parse --short HEAD)}"
BUCKET_NAME="${TF_STATE_BUCKET:-terraform-state-bucket-${SHORT_SHA}}"
TABLE_NAME="${TF_STATE_LOCK_TABLE:-terraform-locks}"

echo ">>> Backend setup: region=${AWS_REGION}, bucket=${BUCKET_NAME}, table=${TABLE_NAME}"

# create bucket if not exists
if ! aws s3api head-bucket --bucket "${BUCKET_NAME}" 2>/dev/null; then
  echo "Creating S3 bucket ${BUCKET_NAME}..."
  if [ "${AWS_REGION}" = "us-east-1" ]; then
    aws s3api create-bucket \
      --bucket "${BUCKET_NAME}" \
      --region "${AWS_REGION}"
  else
    aws s3api create-bucket \
      --bucket "${BUCKET_NAME}" \
      --region "${AWS_REGION}" \
      --create-bucket-configuration LocationConstraint="${AWS_REGION}"
  fi

  aws s3api put-bucket-versioning \
    --bucket "${BUCKET_NAME}" \
    --versioning-configuration Status=Enabled
else
  echo "S3 bucket ${BUCKET_NAME} already exists."
fi

# create dynamodb table if not exists
if ! aws dynamodb describe-table --table-name "${TABLE_NAME}" 2>/dev/null; then
  echo "Creating DynamoDB table ${TABLE_NAME}..."
  aws dynamodb create-table \
    --table-name "${TABLE_NAME}" \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
else
  echo "DynamoDB table ${TABLE_NAME} already exists."
fi

echo ">>> Backend setup done."
