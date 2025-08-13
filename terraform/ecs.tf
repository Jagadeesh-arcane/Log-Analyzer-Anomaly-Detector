resource "aws_ecs_cluster" "log_analyzer_cluster" {
  name = "${var.project_name}-cluster"
  tags = var.tags
}

resource "aws_ecs_task_definition" "log_analyzer_task" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"

  container_definitions = jsonencode([{
    name      = "${var.project_name}"
    image     = "${aws_ecr_repository.log_analyzer_repo.repository_url}:${var.image_tag}"
    essential = true
    portMappings = [{
      containerPort = var.streamlit_port
      hostPort      = var.streamlit_port
    }]
    environment = [
      { name = "EMAIL_USER", value = var.email_user },
      { name = "EMAIL_PASSWORD", value = var.email_password },
      { name = "EMAIL_HOST", value = var.email_host },
      { name = "EMAIL_PORT", value = tostring(var.email_port) },
      { name = "ALERT_EMAIL_TO", value = var.alert_email_to },
      { name = "LOG_FILE_PATH", value = var.log_file_path },
      { name = "SENDER_NAME", value = var.sender_name },
      { name = "RESPONSE_TIME_THRESHOLD", value = tostring(var.response_time_threshold) },
      { name = "STREAMLIT_PORT", value = tostring(var.streamlit_port) }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/${var.project_name}"
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])

  execution_role_arn = aws_iam_role.ecs_task_exec_role.arn

  tags = var.tags
}

resource "aws_ecs_service" "log_analyzer_service" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.log_analyzer_cluster.id
  task_definition = aws_ecs_task_definition.log_analyzer_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = module.vpc.public_subnets
    assign_public_ip = true
    security_groups  = [aws_security_group.ecs_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app_tg.arn
    container_name   = var.project_name
    container_port   = var.streamlit_port
  }

  depends_on = [
    aws_iam_role_policy_attachment.ecs_task_exec_policy,
    aws_lb_listener.http_listener
  ]

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 7
  tags              = var.tags
}
