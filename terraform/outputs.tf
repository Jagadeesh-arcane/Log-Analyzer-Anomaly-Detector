output "ecr_repository_url" {
  value = aws_ecr_repository.log_analyzer_repo.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.log_analyzer_cluster.name
}

output "ecs_service_name" {
  value = aws_ecs_service.log_analyzer_service.name
}

output "alb_dns_name" {
  value = aws_lb.app_alb.dns_name
}

output "web_app_url" {
  value = "http://${aws_lb.app_alb.dns_name}:${var.streamlit_port}"
}
