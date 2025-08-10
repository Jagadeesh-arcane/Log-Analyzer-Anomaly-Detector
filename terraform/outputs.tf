output "app_instance_ip" {
  value = aws_instance.app_instance.public_ip
}
