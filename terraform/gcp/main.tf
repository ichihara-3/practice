terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.62.1"
    }
  }
}

provider "google" {
  credentials = file("credentials.json")
  project     = "wasabi-playground"
  region      = "asia-northeast1"
  zone        = "asia-northeast1-a"
}

resource "google_compute_ne" "vpc_network" {
  name = "vpc-network"
}

