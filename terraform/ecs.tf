resource "aws_ecs_cluster" "log_analyzer_cluster" {
  name = "log-analyzer-cluster"
}

resource "aws_ecs_task_definition" "log_analyzer_task" {
  family                   = "log-analyzer-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"

  container_definitions = jsonencode([{
    name  = "log-analyzer"
    image = "${aws_ecr_repository.log_analyzer_repo.repository_url}:${var.image_tag}"
    essential = true
    portMappings = [{
      containerPort = 8501
      hostPort      = 8501
    }]
    environment = [
      { name = "EMAIL_USER", value = var.email_user },
      { name = "EMAIL_PASSWORD", value = var.email_password }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/log-analyzer"
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])

  execution_role_arn = aws_iam_role.ecs_task_exec_role.arn
  cpu                = "512"
  memory             = "1024"
}

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

  depends_on = [aws_iam_role_policy_attachment.ecs_task_exec_policy]
}

resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/log-analyzer"
  retention_in_days = 7
}
