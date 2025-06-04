# 🚗 Car Rental System API

**Automobilių nuomos sistemos** backend dalis, skirta darbuotojų ir visų vidinių procesų valdymui.

- Sukurta su **FastAPI**
- Naudojama **JWT autentifikacija**
- „Layered architecture“
- HATEOAS nuorodos pagal Richardson Maturity Model 4 lygį
- Modernios REST API praktikos

---

## 🔗 Pagrindiniai resursai

| Resursas           | Endpointas           | Aprašas                        |
|--------------------|---------------------|--------------------------------|
| Autentifikacija    | `/auth`             | Prisijungimas, registracija    |
| Darbuotojai        | `/employees`        | Darbuotojų valdymas            |
| Klientai           | `/clients`          | Klientų valdymas               |
| Automobiliai       | `/cars`             | Automobilių valdymas           |
| Užsakymai          | `/orders`           | Užsakymų valdymas              |
| Rezervacijos       | `/reservations`     | Rezervacijų valdymas           |
| Sąskaitos          | `/invoices`         | Sąskaitų generavimas           |
| Geokodavimas       | `/geocode`          | Adreso konvertavimas į koordinates |
| Klientų palaikymas | `/support`          | Pagalbos užklausos             |

---

## ♻️ Architektūra

```
[ FastAPI endpoints ]
        │
        ▼
[ Schemos (input/output) ] ➞ [ Repozitorijos (CRUD) ] ➞ [ Paslaugos (verslo logika, JWT, hash) ]
        │
        ▼
 [ DB Modeliai (SQLAlchemy) ]
```

---

## 📂 Kodo struktūra

```
autorent_api/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/endpoints/
│   │       ├── auth.py
│   │       ├── car.py
│   │       ├── client.py
│   │       ├── client_support.py
│   │       ├── employee.py
│   │       ├── geocode.py
│   │       ├── invoice.py
│   │       ├── order.py
│   │       └── reservation.py
│   ├── db/
│   │   ├── session.py
│   │   └── base.py
│   ├── models/
│   │   ├── car.py
│   │   ├── client.py
│   │   ├── client_support.py
│   │   ├── employee.py
│   │   ├── geocode.py
│   │   ├── invoice.py
│   │   ├── location.py
│   │   ├── order.py
│   │   └── reservation.py
│   ├── repositories/
│   │   ├── car.py
│   │   ├── client.py
│   │   ├── client_support.py
│   │   ├── employee.py
│   │   ├── geocode.py
│   │   ├── invoice.py
│   │   ├── order.py
│   │   └── reservation.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── car.py
│   │   ├── client.py
│   │   ├── client_support.py
│   │   ├── employee.py
│   │   ├── geocode.py
│   │   ├── invoice.py
│   │   ├── order.py
│   │   └── reservation.py
│   ├── services/
│   │   └── auth_service.py
│   ├── utils/
│   │   └── hateoas.py
│   └── api/deps.py
├── init_db.sql
├── .env.example
└── requirements.txt
```

---

## 📘 Svarbiausi endpoint’ai

<details>
<summary><strong>Autentifikacija</strong></summary>

- `POST   /api/v1/auth/login` – prisijungimas (JWT)
- `POST   /api/v1/auth/register` – naujo darbuotojo registracija
- `POST   /api/v1/auth/logout` – atsijungimas (placeholder)
- `GET    /api/v1/auth/me` – savo profilis
- `POST   /api/v1/auth/change-password` – keisti slaptažodį

</details>

<details>
<summary><strong>Darbuotojai</strong></summary>

- `GET    /api/v1/employees/` – visi darbuotojai
- `GET    /api/v1/employees/{id}` – vienas darbuotojas
- `POST   /api/v1/employees/` – sukurti naują
- `PUT    /api/v1/employees/{id}` – atnaujinti
- `DELETE /api/v1/employees/{id}` – pašalinti

</details>

<details>
<summary><strong>Klientai</strong></summary>

- `GET    /api/v1/clients/` – visi klientai
- `GET    /api/v1/clients/{id}` – vienas klientas
- `POST   /api/v1/clients/` – sukurti naują
- `PUT    /api/v1/clients/{id}` – atnaujinti
- `DELETE /api/v1/clients/{id}` – pašalinti
- `GET    /api/v1/clients/{id}/orders` – kliento užsakymai

</details>

<details>
<summary><strong>Automobiliai</strong></summary>

- `GET    /api/v1/cars/` – visi automobiliai
- `GET    /api/v1/cars/{id}` – konkretus automobilis
- `POST   /api/v1/cars/` – sukurti naują
- `PUT    /api/v1/cars/{id}` – atnaujinti
- `PATCH  /api/v1/cars/{id}/status` – keisti būseną
- `DELETE /api/v1/cars/{id}` – pašalinti
- `GET    /api/v1/cars/search` – filtravimas

</details>

<details>
<summary><strong>Užsakymai</strong></summary>

- `GET    /api/v1/orders/` – visi užsakymai
- `GET    /api/v1/orders/{id}` – vienas užsakymas
- `POST   /api/v1/orders/` – sukurti naują
- `PUT    /api/v1/orders/{id}` – atnaujinti
- `DELETE /api/v1/orders/{id}` – pašalinti
- `GET    /api/v1/orders/stats/by-status` – statistika pagal būseną
- `GET    /api/v1/orders/by-client/{kliento_id}` – kliento užsakymai

</details>

<details>
<summary><strong>Rezervacijos</strong></summary>

- `GET    /api/v1/reservations/` – visos rezervacijos
- `GET    /api/v1/reservations/latest` – naujausios rezervacijos
- `GET    /api/v1/reservations/{id}` – viena rezervacija
- `POST   /api/v1/reservations/` – sukurti naują
- `PUT    /api/v1/reservations/{id}` – atnaujinti
- `DELETE /api/v1/reservations/{id}` – pašalinti
- `GET    /api/v1/reservations/search` – paieška

</details>

<details>
<summary><strong>Sąskaitos (invoices)</strong></summary>

- `GET    /api/v1/invoices/` – visos sąskaitos
- `POST   /api/v1/invoices/` – sukurti naują
- `DELETE /api/v1/invoices/{id}` – pašalinti
- `PATCH  /api/v1/invoices/{id}/status` – keisti statusą

</details>

<details>
<summary><strong>Geokodavimas</strong></summary>

- `POST   /api/v1/geocode` – adresas → lat/lng

</details>

<details>
<summary><strong>Klientų palaikymas</strong></summary>

- `GET    /api/v1/support/` – visos užklausos
- `POST   /api/v1/support/` – sukurti
- `GET    /api/v1/support/unanswered` – neatsakytos
- `GET    /api/v1/support/{id}` – viena užklausa
- `PATCH  /api/v1/support/{id}` – atsakyti/atnaujinti
- `DELETE /api/v1/support/{id}` – pašalinti

</details>

---

## ⚙️ Paleidimo instrukcija

### 1. Klonavimas ir priklausomybės:

```bash
git clone https://github.com/gabwowce/autorent_api
cd autorent_api
pip install -r requirements.txt
```

### 2. `.env` failo paruošimas:

1. Nukopijuok `.env.example` į `.env`:

```bash
cp .env.example .env
```

2. Atidaryk `.env` failą redaktoriuje (pvz. VSCode):

3. Rask eilutę:

```
DATABASE_URL=
```

4. Pakeisk į savo duomenų bazės prisijungimą, pvz.:

```
DATABASE_URL=mysql+pymysql://root:12301@localhost:3306/autorentdb
```

📌 Prisijungimo duomenys turi atitikti tavo MySQL naudotoją, slaptažodį ir bazės pavadinimą.

---

### 3. Duomenų bazės paruošimas:

1. Įsitikink, kad veikia MySQL serveris. Galimos aplinkos:

   - 🟢 **XAMPP**, **MAMP**, **WAMP** (Windows/Mac lokalūs serveriai)
   - 🟢 **MySQL Workbench**, **DBeaver** (grafiniai klientai)
   - 🟢 **phpMyAdmin** (per naršyklę)
   - 🟢 **MySQL CLI** (komandinė eilutė)

2. Sukurk duomenų bazę:
   - Per CLI:

```sql
CREATE DATABASE autorentdb;
```

- Arba GUI (pvz. DBeaver) ➝ „New Database“

3. Įrašyk duomenis iš failo:

```bash
mysql -u root -p autorentdb < init_db.sql
```

- `-u root` – tavo MySQL naudotojas
- `-p` – paprašys slaptažodžio
- `autorentdb` – bazės pavadinimas

✅ Jei pavyko – nematysi klaidų, o duomenys bus matomi GUI ar CLI.

---

### 4. API paleidimas:

```bash
uvicorn app.main:app --reload
```

🧪 Swagger: http://localhost:8000/docs

---

## 👥 Darbo su šakomis eiga

1. Naujos šakos kūrimas:

```bash
git checkout -b feature/orders-endpoints
```

2. Įkėlimas į GitHub:

```bash
git add .
git commit -m "Sukurtas orders CRUD"
git push origin feature/orders-endpoints
```

3. Pull request:
   - Eik į GitHub ➝ tavo šaka ➝ „Compare & pull request“ ➝ Merge

📌 `main` apsaugotas nuo tiesioginio push

---

## 🧱 Naujo endpoint kūrimo gidas

1. `models/` ➝ SQLAlchemy modelis
2. `schemas/` ➝ `ModelCreate`, `ModelUpdate`, `ModelOut`
3. `repositories/` ➝ CRUD logika
4. `endpoints/` ➝ FastAPI route'ai
5. `main.py` ➝ router registracija:

```python
from app.api.v1.endpoints import orders
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
```

6. Testavimas per Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

---

✅ Jei viską padarei teisingai – paleisi API su testiniais duomenimis.

🛠️ Reikia pagalbos? Susisiek su projekto architektu.

---

2026