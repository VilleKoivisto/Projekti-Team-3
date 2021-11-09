
CREATE DATABASE Tuntikirjausohjelma;

\c tuntikirjausohjelma;


CREATE TABLE Tuntikirjaus (Id SERIAL PRIMARY KEY, 
    Nimi VARCHAR(255) NOT NULL,
    Aloituspvm date NOT NULL,
    Aloitusaika time NOT NULL, 
    Lopetuspvm date NOT NULL,
    Lopetusaika time NOT NULL,
    Projekti VARCHAR(255) NOT NULL,
    Selite VARCHAR(255)
);

