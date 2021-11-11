""" Init-tiedoston parseri """

from configparser import ConfigParser
import os

koti = os.path.expanduser('~')

def parseri(tiedosto=f'{koti}/frontendfolder/data/database.ini', kentta='postgresql'):
    """ Käsittele asetustiedosto: database.ini """

    parseri = ConfigParser()
    parseri.read(tiedosto)
    db = {}

    if parseri.has_section(kentta):
        params = parseri.items(kentta)
        
        for param in params:
            db[param[0]] = param[1]
    
    else:
        raise Exception('Kenttää {0} ei löydy tiedostosta: {1}'.format(kentta, tiedosto))
    
    return db