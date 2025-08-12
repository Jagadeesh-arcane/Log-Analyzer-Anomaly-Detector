provider "aws" {
  region  = var.aws_region
}

# ------------------------------
# ECR Repository
# ------------------------------
resource "aws_ecr_repository" "log_analyzer_repo" {
  name                 = "log-analyzer"
  image_tag_mutability = "MUTABLE"
}

# ------------------------------
# VPC + Networking
# ------------------------------
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.2"

  name = "log-analyzer-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]

  enable_dns_hostnames = true
  enable_dns_support   = true
}

# ------------------------------
# Security Group for ALB & ECS
# ------------------------------
resource "aws_security_group" "ecs_sg" {
  name        = "log-analyzer-sg"
  description = "Allow HTTP inbound traffic"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ------------------------------
# ECS Cluster
# ------------------------------
resource "aws_ecs_cluster" "log_analyzer_cluster" {
  name = "log-analyzer-cluster"
}

# ------------------------------
# ECS Task Definition
# ------------------------------
resource "aws_ecs_task_definition" "log_analyzer_task" {
  family                   = "log-analyzer-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"

  container_definitions = jsonencode([{
    name      = "log-analyzer"
    image     = "${aws_ecr_repository.log_analyzer_repo.repository_url}:latest"
    essential = true
    portMappings = [{
      containerPort = 8501
      hostPort      = 8501
    }]
    environment = [
      { name = "EMAIL_USER", value = var.email_user },
      { name = "EMAIL_PASSWORD", value = var.email_password }
    ]
  }])

  execution_role_arn = aws_iam_role.ecs_task_exec_role.arn
}

# ------------------------------
# IAM Role for ECS Task Execution
# ------------------------------
resource "aws_iam_role" "ecs_task_exec_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_exec_policy" {
  role       = aws_iam_role.ecs_task_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ------------------------------
# ECS Service
# ------------------------------
resource "aws_ecs_service" "log_analyzer_service" {
  name            = "log-analyzer-service"
  cluster         = aws_ecs_cluster.log_analyzer_cluster.id
  task_definition = aws_ecs_task_definition.log_analyzer_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = module.vpc.public_subnets
    assign_public_ip = true
    security_groups  = [aws_security_group.ecs_sg.id]
  }
}
