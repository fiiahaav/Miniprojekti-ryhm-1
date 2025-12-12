# Miniprojekti-ryhm-1
Ohjelmistotuotanto miniprojekti - Viitteidenhallintasovellus

[![CI pipeline](https://github.com/fiiahaav/Miniprojekti-ryhm-1/actions/workflows/test.yml/badge.svg)](https://github.com/fiiahaav/Miniprojekti-ryhm-1/actions/workflows/test.yml)

[Product-backlog](https://docs.google.com/spreadsheets/d/1dKQkSXH3QKJ_fpU7lTmOB-eHB5XSrer6C5ilD1vwazk/edit?gid=1#gid=1)

[Sprint-backlog](https://docs.google.com/spreadsheets/d/1dKQkSXH3QKJ_fpU7lTmOB-eHB5XSrer6C5ilD1vwazk/edit?gid=8#gid=8)

[Testikattavuusraportti](http://htmlpreview.github.io/?https://github.com/fiiahaav/Miniprojekti-ryhm-1/blob/testit/index.html)

## Asennus ja käyttöönotto

### 1. Vaatimukset

- Python 3.12 tai uudempi
- Poetry 2.2.1 tai uudempi
- PostgreSQL-tietokanta

### 2. Asenna riippuvuudet

```bash
poetry install
```

### 3. Luo tietokanta PostgreSQL:ään

```bash
sudo -u postgres psql -c "CREATE DATABASE <tietokanta>;"
```

### 4. Luo ympäristömuuttujat

Luo projektin juureen `.env`-tiedosto ja lisää tiedostoon seuraavat rivit:

```
DATABASE_URL=postgresql+psycopg2://<käyttäjä>:<salasana>@localhost:5432/<tietokanta>
SECRET_KEY=<oma_salainen_avain>
TEST_ENV=true
```

Korvaa `<käyttäjä>`, `<salasana>` ja `<tietokanta>` omilla PostgreSQL-tietokantasi tiedoilla.


### 5. Alusta tietokantataulut

```bash
poetry run python src/db_helper.py
```

### 5. Käynnistä sovellus

```bash
poetry run python src/index.py
```

Sovellus käynnistyy osoitteeseen: http://localhost:5000

## Testaus

### Yksikkötestit

```bash
poetry run pytest
```

### Robot Framework -testit

```bash
poetry run robot src/story_tests
```

## Definition of Done

- Toiminnallisuus toimii, niin kuin sovittu asiakkaan kanssa.
  
- Toiminnallisuus on testattavissa.
  
- Testit menevät läpi.
