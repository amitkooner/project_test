variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-east1"
}

variable "data_lake_bucket_name" {
  description = "The name of the Cloud Storage bucket for the data lake"
  type        = string
}

variable "bq_dataset_name" {
  description = "The name of the BigQuery dataset"
  type        = string
}