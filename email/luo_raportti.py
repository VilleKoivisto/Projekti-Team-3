import datetime
from hae_rivit import sql_hae_rivit
from hae_lampotila import hae_lampo

""" indeksit:
Muuttuja "rivit" sisältää tietokannan rivit (tuple) listassa.
Listasta iteroitujen rivituplien indeksit:

1 = nimi, 2 = al pvm, 3 = al aika, 4 = lop pvm, 5 = lop aika, 6 = projekti, 7 = selite
"""

def luo(waether_api_key):
    """ Luo rivitetyn merkkijonon sähköpostin viestikenttää varten """

    rivit = sql_hae_rivit()
    
    kooste = ""
    kokonaistunnit_des = 0
    max_lampo = hae_lampo(waether_api_key)

    for kirjaus in rivit:
        # Yhdistetään date- ja time-objektit & lasketaan aloitus- ja lopetusaikojen väliin jäävät tunnit
        aloitus = datetime.datetime.combine(kirjaus[2], kirjaus[3])
        lopetus = datetime.datetime.combine(kirjaus[4], kirjaus[5])
        
        # Muutetaan datetime-objektien erotus sekunneiksi ja erotetaan tunnit ja minuutit
        tunnit_des = abs(lopetus - aloitus).total_seconds() / 3600
        tunti, minuutti = divmod(tunnit_des, 1)

        # Lisätään rivin tunnit saldoon
        kokonaistunnit_des += tunnit_des

        # Lisätään kirjausrivit koosteeseen
        kooste += f'Konsultti: {kirjaus[1]}\n'
        kooste += f'Aloitusaika: {aloitus.strftime("%d.%m.%Y (%H:%M)")}\n'
        kooste += f'Lopetusaika: {lopetus.strftime("%d.%m.%Y (%H:%M)")}\n'
        kooste += f'Projekti: {kirjaus[6]}\n'
        kooste += f'Selite: "{kirjaus[7]}"\n'
        kooste += f'Tunnit: {int(tunti)} h {int(minuutti * 60)} min\n\n'

    # Erotetaan kokonaistunnit ja -minuutit
    kok_tunti, kok_minuutti = divmod(kokonaistunnit_des, 1)

    # Lopuksi kokonaistunnit ja lämpötila
    kooste += f"Työhön käytetyt tunnit yhteensä: {int(kok_tunti)} h {int(kok_minuutti * 60)} min\nLämpötila lähetyshetkellä: {max_lampo} C"

    return kooste