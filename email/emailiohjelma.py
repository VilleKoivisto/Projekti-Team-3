## kirjastot

# sähköposti
import smtplib
# sää
import requests
import json
# muut
from datetime import date

## configuroi emailin lähetyksen

server = smtplib.SMTP('smtp.gmail.com', 587)

server.ehlo()
server.starttls()
server.ehlo()

## avaa emailin tiedot (käyttis ja salis) erillisestä tiedostosta, joka on gitignoressa

with open(".emailsalaisuuksia","r") as f:
    lines2 = []
    lines = f.readlines()
    for i in range(len(lines)): ## poistaa newlinet
        lines2.append(lines[i].strip('\n'))
    emaili = lines2[0]
    passu = lines2[1]
    f.close()

# print(emaili) # testiprinttejä
# print(passu) # testiprinttejä

## kirjausdata mock, tähän tulee myöhemmin haku databasesta siltä päivältä milloin CRON-jobi suoritetaan
## tähän myöhemmin looppi, että tunkee kaikki databasen tietyn päivän tiedot listaan tai sanakirjaan,
## että ne voi kirjoittaa spostiviestiin

aloituspvm = "9.11.2021"
aloitusaika = "08:00"
lopetuspvm = "9.11.2021"
lopetusaika = "16:00"
projektinimi = "Projekti"
selite = "Sikasaikku"
tuntisumma = 25
subjectdate = date.today()

## säätietojen haku

api_key = "xxx"
zippikoodi = "00100" ## Helsinki / Kaisaniemi (todnäk)
countrykoodi = "fi"
langikoodi = "fi"
url = "https://api.openweathermap.org/data/2.5/weather?zip=%s,%s&appid=%s&units=metric" % (zippikoodi, countrykoodi, api_key)
response = requests.get(url)
data = json.loads(response.text)
lampotila_max = data['main']['temp_max']

## varsinainen sähköpostin lähetys, tähän myöhemmin looppi että iteroi spostiviestiin kaikki kirjaukset listasta

server.login(emaili, passu)
sender_email = emaili
receiver_email = "voicehaustmi@gmail.com"
message = f"Subject: Emailraportti, {subjectdate}" \
            f"\n" + "\n" \
            f"Aloituspvm- ja aika: {aloituspvm}, klo {aloitusaika} \n" \
            f"Lopetuspvm- ja aika: {lopetuspvm}, klo {lopetusaika} \n" \
            f"Projektinimi: {projektinimi} \n" \
            f"Selite: {selite}" \
            f"\n" + "\n" \
            f"Tuntisumma: {tuntisumma}" \
            f"\n" \
            f"------------------------" \
            f"\n" \
            f"Hki (Kaisaniemen havaintoasema) celsiukset on {lampotila_max} C"

server.sendmail(sender_email, receiver_email, message)
