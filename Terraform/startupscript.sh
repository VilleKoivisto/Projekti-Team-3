#! /bin/bash/

# root userille menevät tarvittavat jutut

sudo apt-get update && sudo apt-get -y install --upgrade python-pip && sudo apt-get -y install postgresql-client && sudo apt-get install unzip && sudo apt-get -y install --upgrade python3-pip && pip3 install --upgrade pip

# lokaalit tarvittavat kirjastot eli meidän versio "requirements.txt"-tiedostosta, tähän ei at-merkkeja koska voi tulla virheilmoja

pip3 install psycopg2
pip3 install requests

#haetaan bucketista zip-tiedostot, unzipataan ne

sudo gsutil cp gs://projektikoodit/Backend.zip .
sudo gsutil cp gs://projektikoodit/Frontend.zip .
sudo unzip Backend.zip -d ./backendfolder
sudo unzip Frontend.zip -d ./frontendfolder

#lisää cronjobin ilman että avaa editoria tms. muutenkaan tarvitsee hyväksyntää terminaalista

sudo echo "0 0 * * * python3 backendfolder/emailiohjelma.py" | crontab
