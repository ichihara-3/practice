terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.62.1"
    }
  }

  backend "gcs" {
    bucket  = "wasabi-playground-tf-backend"
    prefix  = "terraform/state"
  }
}

provider "google" {
  credentials = file("credentials.json")
  project     = "wasabi-playground"
  region      = "asia-northeast1"
  zone        = "asia-northeast1-a"
}

resource "google_storage_bucket" "bucket" {
  name          = "wasabi-playground-tf-backend"
  location      = "asia-northeast1"
  storage_class = "REGIONAL"
}


