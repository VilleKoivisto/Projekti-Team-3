"""
Hakee tietokannasta rivejä.
"""

import psycopg2
from hae_rivit_config import parseri

# Sisään tuleva data
# nimi, aloituspvm, aloitusaika, lopetuspvm, lopetusaika, projekti, selite

def sql_hae_rivit():
    """
    Hae rivit
    """

    yhteys = None
    taulu = 'tuntikirjaus'  # pitäiskö tän tulla jostain muualta vai olla kovakoodattu?

    try:
        yhteys = psycopg2.connect(**parseri())
        kursori = yhteys.cursor()
        
        SQL = f"SELECT * FROM {taulu};"
        
        kursori.execute(SQL)
        kaikki_data = kursori.fetchall()
        
        kursori.close()

    except (Exception, psycopg2.DatabaseError) as virhe:
        print(virhe)

    finally:
        if yhteys is not None:
            yhteys.close()
    
    return kaikki_data