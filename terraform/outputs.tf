# Outputs
output "app_instance_ip" {
  description = "Public IP of EC2 instance"
  value = aws_instance.app_instance.public_ip
}

output "app_instance_dns" {
  description = "Public DNS of EC2 instance"
  value = aws_instance.app_instance.public_dns
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app_repo.repository_url
}
