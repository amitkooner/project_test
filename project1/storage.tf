resource "google_storage_bucket" "data_lake_bucket" {
  name                        = var.data_lake_bucket_name
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}