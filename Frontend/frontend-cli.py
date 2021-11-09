"""
Projektitehtävä / ryhmä 3 / Frontendin päätiedosto
Frontend vastaanottaa käyttäjältä tuntikirjauksia ja tallentaa ne kantaan (vapaavalintainen tiedontallennusformaatti GCP:ssä)
Tuntikirjaukset yms. annetaan parametreinä pääfunktiolle
"""

#TODO: syötteen validointi
#TODO: tietokantaan yhteys
#TODO: syöte tietokantaan


import argparse
import psycopg2
from datetime import datetime


def validoi_data():
    pass


def main(kayttaja_id, aloitus_pvm, aloitus_aika, lopetus_pvm, lopetus_aika, projekti_nimi, selite):
    """ Pääfunktio josta käsin suoritetaan muut jutut """

    # TESTI:
    print(kayttaja_id)
    print(aloitus_pvm)


if __name__ == "__main__":

    # Alustetaan parseri
    parser = argparse.ArgumentParser()

    # Lisätään argumentit
    parser.add_argument("kayttaja_id")
    parser.add_argument("aloitus_pvm")
    parser.add_argument("aloitus_aika")
    parser.add_argument("lopetus_pvm")
    parser.add_argument("lopetus_aika")
    parser.add_argument("projekti_nimi")
    parser.add_argument("selite")

    # Käsitellään argumentit
    argu = parser.parse_args()

    # Viedään argumentit mainiin
    main(argu.kayttaja_id, argu.aloitus_pvm, argu.aloitus_aika, argu.lopetus_pvm, argu.lopetus_aika, argu.projekti_nimi, argu.selite)