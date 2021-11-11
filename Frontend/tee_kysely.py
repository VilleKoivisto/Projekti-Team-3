"""
Database queries with Python, simple basics
"""

import psycopg2
from kysely_config import parseri

# Sisään tuleva data
# nimi, aloituspvm, aloitusaika, lopetuspvm, lopetusaika, projekti, selite

def sql_lisaa_rivi(nimi, aloituspvm, aloitusaika, lopetuspvm, lopetusaika, projekti, selite):
    """
    Lisää rivi tauluun
    """

    yhteys = None
    taulu = 'tuntikirjaus'  # pitäiskö tän tulla jostain muualta vai olla kovakoodattu?

    try:
        yhteys = psycopg2.connect(**parseri())
        kursori = yhteys.cursor()

        SQL = f"INSERT INTO {taulu} (nimi, aloituspvm, aloitusaika, lopetuspvm, lopetusaika, projekti, selite) VALUES (%s,%s,%s,%s,%s,%s,%s);"
        arvot = (nimi, aloituspvm, aloitusaika, lopetuspvm, lopetusaika, projekti, selite)
        
        kursori.execute(SQL, arvot)
        yhteys.commit()
        kursori.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

        return False

    finally:
        if yhteys is not None:
            yhteys.close()
    
    return True