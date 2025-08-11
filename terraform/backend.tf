terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket-6546768"
    key            = "log-analyzer-anomaly-detector-public/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
