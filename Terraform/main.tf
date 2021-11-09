# Projekti / ryhmä 3 / Terraform-template
# -----------------------------------------------

# Templaten muuttujat määritellään tiedostossa "variables.tf"

# Provider-tiedot:
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
    postgresql = {
      source = "cyrilgdn/postgresql"
      version = "1.14.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project = var.project
  region  = var.region
  zone    = var.zone
}

# Projektin resurssit:
# Luo VPC:n nimeltä tuntikirjaus-vpc
resource "google_compute_network" "vpc_network" {
  project = var.project
  name = "tuntikirjaus-vpc"
  auto_create_subnetworks = false
}

# Luo tuntikirjaus-vpc:lle aliverkon tuntikirjaus-sub-fin, jossa 2 (käytettävissä olevaa) ip-osoitetta
resource "google_compute_subnetwork" "public-subnetwork" {
    name = "tuntikirjaus-sub-fin"
    ip_cidr_range = "10.0.0.0/29"
    region = var.region
    network = google_compute_network.vpc_network.name
}

# Luo SQL database instancen annetuilla tiedoilla

resource "google_sql_database_instance" "Postgresqlinstanssi" {
  name             = "postgresqlinstanssi5367415439"
  database_version = "POSTGRES_13"
  region           = var.region

  settings {
    tier            = "db-f1-micro" # postgresql tukee vain shared core machineja! tämä shared-core löytyy haminasta
  }
}

resource "google_sql_user" "postgres" {
  project  = var.project
  name     = var.sql_name
  instance = google_sql_database_instance.Postgresqlinstanssi.name
  password = var.sql_password
}

provider "postgresql" {
  scheme   = "gcppostgres"
  host     = google_sql_database_instance.Postgresqlinstanssi.connection_name
  username = google_sql_user.postgres.name
  password = google_sql_user.postgres.password
}