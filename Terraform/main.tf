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

# Luo tuntikirjaus-vpc:lle aliverkon tuntikirjaus-sub-fin
resource "google_compute_subnetwork" "public-subnetwork" {
    name = "tuntikirjaus-sub-fin"
    ip_cidr_range = "10.0.0.0/27"
    region = var.region
    network = google_compute_network.vpc_network.name
}

# Firewall-resurssit

# SSH-yhteydet auki
resource "google_compute_firewall" "allow_ssh" {
  name        = "allow-ssh"
  network     = google_compute_network.vpc_network.name
  direction   = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  target_tags = ["ssh-enabled"]
}

# allokoi private ip osoitteet vpc:hen 
resource "google_compute_global_address" "private_ip_do" {
  name         = "private-ip"
  purpose      = "VPC_PEERING"
  address_type = "INTERNAL"
  ip_version   = "IPV4"
  prefix_length = 24
  network       = google_compute_network.vpc_network.self_link
}

# enabloi private services access
resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc_network.self_link
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_do.name]
}

# Luo SQL database instancen annetuilla tiedoilla

resource "google_sql_database_instance" "PostgresqlYenCHQMtfr" { # Jos cloud sql instanssi on tehty ja deletoitu/destroyattu, ei voi käyttää samaa instanssin nimeä viikkoon!
  name             = "postgresqlinstanssi"
  database_version = "POSTGRES_13"
  depends_on       = [google_service_networking_connection.private_vpc_connection]
  region           = var.region

  settings {
    tier            = "db-f1-micro" # postgresql tukee vain shared core machineja! tämä shared-core löytyy haminasta
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc_network.self_link
    }
  }
}

resource "google_sql_user" "postgres" {
  project  = var.project
  name     = var.sql_name
  instance = google_sql_database_instance.PostgresqlYenCHQMtfr.name
  password = var.sql_password
}

provider "postgresql" {
  scheme   = "gcppostgres"
  host     = google_sql_database_instance.PostgresqlYenCHQMtfr.connection_name
  username = google_sql_user.postgres.name
  password = google_sql_user.postgres.password

# Luo frontend/backend-instanssin
resource "google_compute_instance" "vm_instance" {
  name         = "tuntikirjaus-instanssi"
  machine_type = "n1-standard-1"
  tags = ["ssh-enabled"]
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    subnetwork = google_compute_subnetwork.public-subnetwork.name
    access_config {
        }
  }
  metadata = {
    enable-oslogin = "TRUE"
  }
  metadata_startup_script = file("startupscript.sh")
  allow_stopping_for_update = true
}
