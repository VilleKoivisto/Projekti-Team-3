import smtplib
from email.message import EmailMessage

# muut
from datetime import date
from luo_raportti import luo
from hae_login_data import hae_data


def main():
    """ Backend: tuntikirjauksista raportin lähettävä email-ohjelma """
    
    # haetaan login-data
    lahettaja_email, vast_ot_email, passu, openweatherapi = hae_data()

    # Luodaan raportti
    kirjausraportti = luo(openweatherapi)

    # alustetaan yhteys
    # Google smtp:
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    server = smtplib.SMTP('smtp.office365.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    # koostetaan sähköposti
    viesti = EmailMessage()
    viesti.set_content(kirjausraportti)

    server.login(lahettaja_email, passu)

    viesti['Subject'] = f"Työtuntiraportti: {date.today()}"
    viesti['From'] = lahettaja_email
    viesti['To'] = vast_ot_email

    server.send_message(viesti)

    server.quit()


if __name__ == "__main__":
    main()