#!/bin/bash
set -e

# install docker and awscli
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -aG docker ec2-user

# install aws-cli v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
unzip /tmp/awscliv2.zip -d /tmp
/tmp/aws/install -i /usr/local/aws-cli -b /usr/local/bin

# login to ECR (will use instance role if available)
AWS_REGION="${region}"
ECR_URL="${ecr_repo_url}"

# Use aws CLI to get login password and docker login
$(/usr/local/bin/aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${ecr_repo_url%/*})

# Pull latest image and run
docker pull ${ecr_repo_url}:latest || true
docker rm -f log-analyzer || true
docker run -d --name log-analyzer -p ${port}:${port} ${ecr_repo_url}:latest
