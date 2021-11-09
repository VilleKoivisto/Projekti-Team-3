"""
Projektitehtävä / ryhmä 3 / Frontendin päätiedosto
Frontend vastaanottaa käyttäjältä tuntikirjauksia ja tallentaa ne kantaan (vapaavalintainen tiedontallennusformaatti GCP:ssä)
Tuntikirjaukset yms. annetaan parametreinä pääfunktiolle
"""

#TODO: tietokantaan yhteys
#TODO: syöte tietokantaan


import argparse
import psycopg2
from datetime import datetime


def validoi_data(args):
    """ Käy läpi syötteen arvot ja validoi, että formaatti on oikea
        - funktio purkaa argumentit listaan jossa indeksi
          0: käyttäjän nimi (str),
          1: aloituspvm (pp/kk/vvvv),
          2: aloitusaika,
          3: lopetuspvm (pp/kk/vvvv),
          4: lopetusaika,
          5: projektin nimi (str),
          6: selite (mitä tulikaan tehtyä, str)
    
    """
    kirjaukset = []

    for arg in args:
        kirjaukset.append(arg)

    # Tarkistetaan onko nimi merkkijono
    if kirjaukset[0].isdigit():
        print(f"Käyttäjänimi ei voi olla numero: {kirjaukset[0]}")
        
        return False

    # tarkistetaan päivämäärien formaatti
    if not tarkista_pvm(kirjaukset[1], kirjaukset[3]):
        print(f"Aloitus- tai lopetuspäivämäärä on väärässä formaatissa: {kirjaukset[1]}, {kirjaukset[3]}")
        print("Oikea formaatti on: pp/kk/vvvv")

        return False

    # tarkistetaan aikojen formaatti
    if not tarkista_aika(kirjaukset[2], kirjaukset[4]):
        print(f"Aloitus- tai lopetusaika on väärässä formaatissa: {kirjaukset[2]}, {kirjaukset[4]}")
        print("Oikea formaatti on: hh:mm")

        return False

    # Tarkistetaan onko projektin nimi merkkijono
    if kirjaukset[5].isdigit():
        print(f"Projektin nimi ei voi olla numero: {kirjaukset[5]}")
        
        return False

    # Tarkistetaan onko selite merkkijono
    if kirjaukset[6].isdigit():
        print(f"Selite ei voi olla numero: {kirjaukset[6]}")
        
        return False

    return True


def tarkista_pvm(*args):
    """ Tarkistaa, onko pvm oikeassa muodossa 
        (validi datetime-objekti)
    """
    
    for arg in args:
        paiva, kuukausi, vuosi = arg.split("/")

        try:
            datetime(int(vuosi), int(kuukausi), int(paiva))

        except ValueError:
            return False
        
    return True


def tarkista_aika(*args):
    """ Tarkistaa, onko aika oikeassa muodossa 
        (validi datetime-objekti)
    """
    
    for arg in args:
        try:
            tunti, minuutti = arg.split(":")
            tunti = int(tunti)
            minuutti = int(minuutti)

            if tunti < 0 or tunti > 23:
                return False

            elif minuutti < 0 or minuutti > 59:
                return False

        except ValueError:
            return False

    return True


def main(*args):
    """ Pääfunktio josta käsin suoritetaan muut jutut """

    # Ohjataan komentoriviargumentit validointifunktioon
    validoi_data(args)


if __name__ == "__main__":
    # Alustetaan parseri
    parser = argparse.ArgumentParser()

    # Lisätään argumentit
    parser.add_argument("kayttaja_nimi")
    parser.add_argument("aloitus_pvm")
    parser.add_argument("aloitus_aika")
    parser.add_argument("lopetus_pvm")
    parser.add_argument("lopetus_aika")
    parser.add_argument("projekti_nimi")
    parser.add_argument("selite")

    # Käsitellään argumentit
    argu = parser.parse_args()

    # Viedään argumentit mainiin
    main(argu.kayttaja_nimi, argu.aloitus_pvm, argu.aloitus_aika, argu.lopetus_pvm, argu.lopetus_aika, argu.projekti_nimi, argu.selite)


# TESTAUKSEEN:
# esimerkkikomento: python .\frontend-cli.py Ville 1/11/2021 8:30 2/11/2021 17:45 Awa-projekti "tein mitä tein"