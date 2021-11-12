# Projekti / ryhmä 3 / Terraformin muuttujat
# --------------------------------------------------

# Nämä haetaan terraform.tfvars-tiedostosta:
variable "project" {}

variable "credentials_file" {}

variable "sql_name" {}

variable "sql_password" {}

# Nämä määritellään tässä:
variable "region" {
    default = "europe-north1"
}

variable "zone" {
    default = "europe-north1-b"
}