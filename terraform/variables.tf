variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "app_name" {
  default = "log-analyzer-anomaly-detector-public"
}

variable "instance_type" {
  description = "EC2 instance type - keep t2.micro/t3.micro for free tier"
  default     = "t2.micro"
}

variable "streamlit_port" {
  default = 8501
}

# Optional: allow overriding VPC id (if you want default)
variable "vpc_id" {
  description = "VPC id (optional) - if not provided, uses default VPC"
  default     = ""
}

variable "public_key_name" {
  description = "Optional keypair name; if you want SSH access (optional)"
  default     = ""
}
