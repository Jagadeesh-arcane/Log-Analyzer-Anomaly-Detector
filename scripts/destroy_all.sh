#!/usr/bin/env bash
set -euo pipefail

AWS_REGION="${AWS_REGION:-us-east-1}"
APP_NAME="${APP_NAME:-${CI_PROJECT_NAME:-log-analyzer-anomaly-detector-public}}"
TF_BACKEND_BUCKET="${TF_STATE_BUCKET:-terraform-state-bucket-${CI_COMMIT_SHORT_SHA}}"
TF_BACKEND_KEY="${TF_STATE_KEY:-${APP_NAME}/terraform.tfstate}"
TF_LOCK_TABLE="${TF_STATE_LOCK_TABLE:-terraform-locks}"

echo ">>> Destroy start: AWS_REGION=${AWS_REGION}, APP_NAME=${APP_NAME}"

# init terraform with backend (so it can read state from S3)
echo "Initializing terraform (S3 backend) ..."
terraform init -backend-config="bucket=${TF_BACKEND_BUCKET}" \
               -backend-config="key=${TF_BACKEND_KEY}" \
               -backend-config="region=${AWS_REGION}" \
               -backend-config="dynamodb_table=${TF_LOCK_TABLE}" || true

# terraform destroy (safe, will use remote state)
echo "Running terraform destroy ..."
terraform destroy -auto-approve -var "aws_region=${AWS_REGION}" -var "app_name=${APP_NAME}" || true

# ECR cleanup (force delete repos that match project name)
echo "Cleaning ECR repositories..."
aws ecr describe-repositories --region "${AWS_REGION}" \
  --query "repositories[?contains(repositoryName, '${APP_NAME}')].repositoryName" --output text | tr '\t' '\n' | while read -r repo; do
    [ -z "${repo}" ] && continue
    echo " -> deleting ECR repo: ${repo}"
    aws ecr delete-repository --repository-name "${repo}" --force --region "${AWS_REGION}" || true
done

# Terminate EC2 instances with Name tag matching APP_NAME
echo "Terminating EC2 instances matching Name=${APP_NAME}..."
aws ec2 describe-instances --region "${AWS_REGION}" \
  --filters "Name=tag:Name,Values=${APP_NAME}*" "Name=instance-state-name,Values=pending,running,stopping,stopped" \
  --query "Reservations[].Instances[].InstanceId" --output text | tr '\t' '\n' | while read -r id; do
    [ -z "${id}" ] && continue
    echo " -> terminating instance ${id}"
    aws ec2 terminate-instances --instance-ids "${id}" --region "${AWS_REGION}" || true
done

# Delete S3 buckets that include APP_NAME
echo "Deleting S3 buckets containing ${APP_NAME}..."
aws s3api list-buckets --query "Buckets[].Name" --output text | tr '\t' '\n' | while read -r bucket; do
  [ -z "${bucket}" ] && continue
  if echo "${bucket}" | grep -q "${APP_NAME}"; then
    echo " -> removing s3://${bucket}"
    aws s3 rb "s3://${bucket}" --force --region "${AWS_REGION}" || true
  fi
done

# Detach and delete IAM role/policies that start with APP_NAME
echo "Cleaning IAM roles & policies..."
aws iam list-roles --query "Roles[?starts_with(RoleName,'${APP_NAME}')].RoleName" --output text | tr '\t' '\n' | while read -r role; do
  [ -z "${role}" ] && continue
  echo " -> processing role ${role}"
  aws iam list-attached-role-policies --role-name "${role}" --query "AttachedPolicies[].PolicyArn" --output text | tr '\t' '\n' | while read -r policy_arn; do
    [ -z "${policy_arn}" ] && continue
    echo "    detaching ${policy_arn}"
    aws iam detach-role-policy --role-name "${role}" --policy-arn "${policy_arn}" || true
  done
  echo "    deleting role ${role}"
  aws iam delete-role --role-name "${role}" || true
done

aws iam list-policies --scope Local --query "Policies[?starts_with(PolicyName,'${APP_NAME}')].Arn" --output text | tr '\t' '\n' | while read -r arn; do
  [ -z "${arn}" ] && continue
  echo " -> deleting policy ${arn}"
  aws iam delete-policy --policy-arn "${arn}" || true
done

echo ">>> Destroy completed."
