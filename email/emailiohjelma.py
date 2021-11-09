## kirjastot

import smtplib
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

aloituspvm = "9.11.2021"
aloitusaika = "08:00"
lopetuspvm = "9.11.2021"
lopetusaika = "16:00"
projektinimi = "Projekti"
selite = "Sikasaikku"
tuntisumma = 25
headerdate = date.today()

## varsinainen sähköpostin lähetys

server.login(emaili, passu)
sender_email = emaili
receiver_email = "voicehaustmi@gmail.com"
message = f"Subject: Emailraportti, {headerdate}" \
            f"\n" + "\n" \
            f"Aloituspvm- ja aika: {aloituspvm}, klo {aloitusaika} \n" \
            f"Lopetuspvm- ja aika: {lopetuspvm}, klo {lopetusaika} \n" \
            f"Projektinimi: {projektinimi} \n" \
            f"Selite: {selite}" \
            f"\n" + "\n" \
            f"Tuntisumma: {tuntisumma}"

server.sendmail(sender_email, receiver_email, message)