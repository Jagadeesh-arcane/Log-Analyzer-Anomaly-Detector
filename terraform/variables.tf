variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "email_user" {
  description = "Email user for app (stored in task env)"
  type        = string
  default     = ""
}

variable "email_password" {
  description = "Email password for app (stored in task env)"
  type        = string
  default     = ""
}

variable "image_tag" {
  description = "Docker image tag pushed to ECR"
  type        = string
  default     = "latest"
}

variable "tf_state_bucket" {
  description = "S3 bucket for terraform state"
  type        = string
  default     = "log-analyzer-tfstate"
}

variable "tf_state_key" {
  description = "S3 key for terraform state"
  type        = string
  default     = "terraform.tfstate"
}

variable "tf_state_lock_table" {
  description = "DynamoDB table for state locks"
  type        = string
  default     = "terraform-locks"
}
