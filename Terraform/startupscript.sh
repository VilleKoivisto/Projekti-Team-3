#! /bin/bash/

sudo apt-get update
# sudo apt-get install python 3.6 # ei tarvitse koska instanssissa on jo valmiiksi asennettuna python
sudo apt-get -y install python-pip
sudo apt-get -y install postgresql-client
sudo pip install psycopg2-binary
sudo gsutil cp gs://projektikoodit/[zippitiedostonnimi].zip .
sudo unzip [zippitiedostonnimi].zip
sudo crontab -e
0 0 * * *  emailiohjelma.py