
CREATE DATABASE tuntikirjausohjelma;

\c tuntikirjausohjelma;


CREATE TABLE tuntikirjaus (Id SERIAL PRIMARY KEY, 
    nimi VARCHAR(255) NOT NULL,
    aloituspvm date NOT NULL,
    aloitusaika time NOT NULL, 
    lopetuspvm date NOT NULL,
    lopetusaika time NOT NULL,
    projekti VARCHAR(255) NOT NULL,
    selite VARCHAR(255)
);

