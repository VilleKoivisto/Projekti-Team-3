#! /bin/bash/

sudo apt-get update
# sudo apt-get install python 3.6 # ei tarvitse koska instanssissa on jo valmiiksi asennettuna python
sudo apt-get -y install python-pip
sudo apt-get -y install postgresql-client
sudo pip install psycopg2-binary