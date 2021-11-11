#! /bin/bash/

sudo apt-get update
sudo apt-get -y install python-pip
sudo apt-get -y install postgresql-client
sudo pip install psycopg2-binary
sudo apt-get install unzip

#haetaan bucketista zip-tiedostot ja unzipataan ne
sudo gsutil cp gs://projektikoodit/Backend.zip .
sudo gsutil cp gs://projektikoodit/Frontend.zip .
sudo unzip Backend.zip
sudo unzip Frontend.zip

#tehdään tiedosto cronhomma, luodaan sinne cronjob (suorittaa emailiohjelma.py:n joka päivä 00:00) ja asennetaan uusi job
sudo crontab -l > cronhomma
sudo echo "0 0 * * *  emailiohjelma.py" >> cronhomma
sudo crontab cronhomma