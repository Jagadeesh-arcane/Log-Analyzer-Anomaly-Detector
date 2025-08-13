variable "project_name" {
  description = "Project name for to deploy resources"
  type        = string
  default     = "log-analyzer"
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS account ID"
  type        = string
  sensitive   = true
}

variable "aws_access_key_id" {
  description = "AWS access key ID"
  type        = string
  sensitive   = true
}

variable "aws_secret_access_key" {
  description = "AWS secret access key"
  type        = string
  sensitive   = true
}

variable "email_user" {
  description = "Email address used for sending alerts"
  type        = string
  sensitive   = true
}

variable "email_password" {
  description = "Password or app-specific password for the email"
  type        = string
  sensitive   = true
}

variable "email_host" {
  description = "SMTP server host"
  type        = string
  default     = "smtp.gmail.com"
}

variable "email_port" {
  description = "SMTP server port"
  type        = number
  default     = 587
}

variable "alert_email_to" {
  description = "Recipient email address for alerts"
  type        = string
  sensitive   = true
}

variable "sender_name" {
  description = "Name shown in sender field of the email"
  type        = string
  default     = "Log-Analyzer"
}

variable "response_time_threshold" {
  description = "Response time threshold in milliseconds"
  type        = number
  default     = 1000
}

variable "streamlit_port" {
  description = "Port on which Streamlit runs"
  type        = number
  default     = 8501
}

variable "log_file_path" {
  description = "Path to the log file to analyze"
  type        = string
  default     = "app/logs/test-3.log"
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

variable "tf_state_bucket" {
  description = "S3 bucket for Terraform state"
  type        = string
  default     = "log-analyzer-tfstate"
}

variable "tf_state_key" {
  description = "Path (key) to Terraform state file in S3"
  type        = string
  default     = "log-analyzer/terraform.tfstate"
}

variable "tf_state_lock_table" {
  description = "DynamoDB table for Terraform state locking"
  type        = string
  default     = "log-analyzer-terraform-locks"
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "Log-Analyzer"
    Environment = "Dev"
    ManagedBy   = "Terraform"
  }
}
