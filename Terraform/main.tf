# Projekti / ryhmä 3 / Terraform-template
# -----------------------------------------------
#TO-DO Lisää firewall-sääntö-tägit instanssiin, kun firewall on luotu! (laini viittä vaille valmiina odottamassa)

# Templaten muuttujat määritellään tiedostossa "variables.tf"

# Provider-tiedot:
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
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

# Luo frontend/backend-instanssin
resource "google_compute_instance" "vm_instance" {
  name         = "tuntikirjaus-instanssi"
  machine_type = "n1-standard-1"
  tags = ["ssh-enabled"]
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
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