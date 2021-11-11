import requests
import json

def hae_lampo(openweatherapi):
    """ Hakee max lämpötilan APIsta """

    api_key = openweatherapi
    zippikoodi = "00100" ## Helsinki / Kaisaniemi (todnäk)
    countrykoodi = "fi"
    url = "https://api.openweathermap.org/data/2.5/weather?zip=%s,%s&appid=%s&units=metric" % (zippikoodi, countrykoodi, api_key)
    
    response = requests.get(url)
    data = json.loads(response.text)

    return data['main']['temp_max']