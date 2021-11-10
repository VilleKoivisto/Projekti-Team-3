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
from tee_kysely import sql_lisaa_rivi


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
        print(f"\nKäyttäjänimi ei voi olla numero: {kirjaukset[0]}\n")
        
        return False

    # tarkistetaan päivämäärien formaatti
    if not tarkista_pvm(kirjaukset[1], kirjaukset[3]):
        print(f"\nAloitus- tai lopetuspäivämäärä on väärässä formaatissa: {kirjaukset[1]}, {kirjaukset[3]}")
        print("Oikea formaatti on: pp-kk-vvvv\n")

        return False

    # tarkistetaan aikojen formaatti
    if not tarkista_aika(kirjaukset[2], kirjaukset[4]):
        print(f"\nAloitus- tai lopetusaika on väärässä formaatissa: {kirjaukset[2]}, {kirjaukset[4]}")
        print("Oikea formaatti on: hh:mm\n")

        return False

    # Tarkistetaan onko projektin nimi merkkijono
    if kirjaukset[5].isdigit():
        print(f"\nProjektin nimi ei voi olla numero: {kirjaukset[5]}\n")
        
        return False

    # Tarkistetaan onko selite merkkijono
    if kirjaukset[6].isdigit():
        print(f"\nSelite ei voi olla numero: {kirjaukset[6]}\n")
        
        return False

    # Tarkistetaan, että alku_pvm aikaisemmin kuin loppupvm
    if not vertaa_pvm(kirjaukset[1], kirjaukset[3]):
        print("\nLopetuspäivämäärä ei voi olla aikaisemmin kuin aloituspäivämäärä.\n")

        return False

    return True


def tarkista_pvm(*args):
    """ Tarkistaa, onko pvm oikeassa muodossa 
        (validi datetime-objekti)
    """

    try:
        for arg in args:
            paiva, kuukausi, vuosi = arg.split("-")

        datetime(int(vuosi), int(kuukausi), int(paiva))

    except ValueError:
        return False
        
    return True


def tarkista_aika(*args):
    """ Tarkistaa, onko aika oikeassa muodossa 
        (validi datetime-objekti)
    """
    
    try:
        for arg in args:
            tunti, minuutti = arg.split(":")

            # value error -testi:
            tunti = int(tunti)
            minuutti = int(minuutti)

            # arvoaluetesti:
            if tunti < 0 or tunti > 23 or minuutti < 0 or minuutti > 59:
                return False

    except ValueError:
        return False

    return True


def vertaa_pvm(alku_pvm, loppu_pvm):
    """ Vertaa päivämääriä:
        aloituspäivän oltava ennen lopetuspäivää
    """

    paiva, kuukausi, vuosi = alku_pvm.split("-")
    alku_dto = datetime(int(vuosi), int(kuukausi), int(paiva))

    paiva, kuukausi, vuosi = loppu_pvm.split("-")
    loppu_dto = datetime(int(vuosi), int(kuukausi), int(paiva))

    if alku_dto > loppu_dto:
        return False

    return True


def main(*args):
    """ Pääfunktio josta käsin suoritetaan muut jutut """

    # Ohjataan komentoriviargumentit validointifunktioon
    if not validoi_data(args):
        return

    else:
        print("\nLisätään rivi tietokantaan...\n")

        kirjaukset = []

        for arg in args:
            kirjaukset.append(arg)

        if not sql_lisaa_rivi(kirjaukset[0], kirjaukset[1], kirjaukset[2], kirjaukset[3], kirjaukset[4], kirjaukset[5], kirjaukset[6]):
            print("\nRiviä ei voitu lisätä...\n")

        else:
            print("\nRivi lisätty tietokantaan.\n")


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
# esimerkkikomento: python .\frontend-cli.py Ville 1-11-2021 8:30 2-11-2021 17:45 Awa-projekti "Pääasia että päivä kuluu..."