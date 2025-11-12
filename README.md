# Car Rental System API

**Automobilių nuomos sistemos** backend dalis, skirta darbuotojų ir visų vidinių procesų valdymui.

- Sukurta su **FastAPI**
- Naudojama **JWT autentifikacija**
- „Layered architecture“
- HATEOAS nuorodos pagal Richardson Maturity Model 4 lygį
- Modernios REST API praktikos

---

## Pagrindiniai resursai

| Resursas             | Endpointas          | Aprašas                        |
|----------------------|---------------------|--------------------------------|
| Autentifikacija      | `/auth`             | Prisijungimas, registracija    |
| Darbuotojai          | `/employees`        | Darbuotojų valdymas            |
| Klientai             | `/clients`          | Klientų valdymas               |
| Automobiliai         | `/cars`             | Automobilių valdymas           |
| Užsakymai            | `/orders`           | Užsakymų valdymas              |
| Rezervacijos         | `/reservations`     | Rezervacijų valdymas           |
| Sąskaitos            | `/invoices`         | Sąskaitų generavimas           |
| Geokodavimas         | `/geocode`          | Adreso konvertavimas į koordinates |
| Klientų aptarnavimas | `/support`          | Pagalbos užklausos             |


---
## Autentifikacijos metodai

| Metodas          | Endpointas                 | Tipas     | Naudojimas             | Aprašymas                                             |
| ---------------- | -------------------------- | --------- | ---------------------- | ----------------------------------------------------- |
| **Local JSON**   | `POST /api/v1/login`       | JSON Body | Frontend               | Vartotojas įveda el. paštą ir slaptažodį JSON formatu |
| **OAuth2 Form**  | `POST /api/v1/token`       | Form-Data | Swagger / CLI          | Swagger sugeneruota forma: `username` ir `password`   |
| **Google OAuth** | `GET /api/v1/google/login` | Redirect  | Išorinis prisijungimas | SSO prisijungimas per Google                          |
| **GitHub OAuth** | `GET /api/v1/github/login` | Redirect  | Išorinis prisijungimas | SSO prisijungimas per GitHub                          |


---
## Vartotojų Rolės ir Leidimai

| Rolė      | Sukūrimo būdas               | Gali Skaityti | Gali Atnaujinti | Gali Trinti |
| --------- | ---------------------------- | ------------- | --------------- | ----------- |
| **Admin** | Rankiniu būdu / DB           | ✅             | ✅               | ✅           |
| **Emplo** | Registracija per `/register` | ✅             | ✅               | ❌           |
| **Guest** | Google/GitHub OAuth          | ✅             | ❌               | ❌           |

## Leidimų tikrinimo mechanizmas
- JWT token’e saugoma sub (el. paštas) ir role
- Middleware (get_current_user) nuskaito šiuos duomenis ir pritaiko leidimus
- Endpointuose naudojamas dekoratorius require_perm(...)

```python
from app.core.permissions import require_perm, Perm

@router.get("/cars/", dependencies=[Depends(require_perm(Perm.VIEW))])
def get_all_cars(): ...

@router.post("/cars/", dependencies=[Depends(require_perm(Perm.EDIT))])
def create_car(): ...

@router.delete("/cars/{id}", dependencies=[Depends(require_perm(Perm.ADMIN))])
def delete_car(): ...
```
---

## Kodo struktūra

```
autorent_api/
├── README.md
├── requirements.txt
├── .gitignore
├── app/
│   ├── .env.example
│   ├── init_db.sql
│   ├── main.py
│   ├── api/
│   │   ├── deps.py
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
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── car.py
│   │   ├── client.py
│   │   ├── client_support.py
│   │   ├── employee.py
│   │   ├── invoice.py
│   │   ├── location.py
│   │   ├── order.py
│   │   ├── reservation.py
│   │   └── __init__.py
│   ├── repositories/
│   │   ├── car.py
│   │   ├── client.py
│   │   ├── client_support.py
│   │   ├── employee.py
│   │   ├── geocode.py
│   │   ├── invoice.py
│   │   ├── order.py
│   │   ├── reservation.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── car.py
│   │   ├── client.py
│   │   ├── client_support.py
│   │   ├── employee.py
│   │   ├── geocode.py
│   │   ├── invoice.py
│   │   ├── location.py
│   │   ├── order.py
│   │   ├── reservation.py
│   │   ├── reservationSummary.py
│   │   └── __init__.py
│   └── services/
│       ├── auth_service.py
│       └── __init__.py
├── docs/
│   └── API_endpoints_plan.md
├── tests/
│   ├── conftest.py
│   ├── init_test_db.sql
│   ├── __init__.py
│   ├── api/
│   │   ├── test_auth.py
│   │   ├── test_car.py
│   │   ├── test_client.py
│   │   ├── test_client_support.py
│   │   ├── test_employee.py
│   │   ├── test_geocode.py
│   │   ├── test_invoice.py
│   │   ├── test_order.py
│   │   ├── test_reservation.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── test_auth_service.py
│   │   └── __init__.py
│   └── utils/
│       ├── test_hateoas.py
│       └── __init__.py
└── utils/
    └── hateoas.py
```

---

## Svarbiausi endpoint’ai

<details>
<summary><strong>Autentifikacija</strong></summary>

**Vietinis prisijungimas**
- `POST   /api/v1/login`            – prisijungimas (JSON body: el_pastas, slaptazodis) → JWT
- `POST   /api/v1/token`            – prisijungimas (form: username, password) – patogu Swagger

**Social OAuth**
- `GET    /api/v1/google/login`     – Google OAuth (pirmą kartą sukuria vartotoją su role `Guest`)
- `GET    /api/v1/github/login`     – GitHub OAuth (pirmą kartą sukuria vartotoją su role `Guest`)

**Vartotojas / slaptažodžiai**
- `POST   /api/v1/auth/register`    – naujo darbuotojo registracija (dažn. Emplo)
- `POST   /api/v1/auth/change-password` – keisti slaptažodį
- `POST   /api/v1/auth/logout`      – atsijungimas (placeholder)
- `GET    /api/v1/auth/me`          – prisijungusio vartotojo profilis

> Pastaba: Swagger „Authorize“ laukelyje įklijuok **tik JWT** (be `Bearer `).
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
- `GET    /api/v1/cars/available` – laisvi automobiliai nurodytu intervalu
- `GET    /api/v1/cars/utilization` – kiek dienų per [from, to) kiekvienas auto turėjo rezervacijų (procentais + dienų skaičius).
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

- `GET    /api/v1/quote` – endpoint’as kainos sąmatai (be rezervacijos kūrimo)
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
<summary><strong>Klientų aptarnavimas</strong></summary>

- `GET    /api/v1/overdue` – endpoint'as ieško „vėluojančių“ užklausų, t. y. neatsakytų ir senesnių nei N val..
- `GET    /api/v1/support/` – visos užklausos
- `POST   /api/v1/support/` – sukurti
- `GET    /api/v1/support/unanswered` – neatsakytos
- `GET    /api/v1/support/{id}` – viena užklausa
- `PATCH  /api/v1/support/{id}` – atsakyti/atnaujinti
- `DELETE /api/v1/support/{id}` – pašalinti

</details>

---

## Paleidimo instrukcija

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

Prisijungimo duomenys turi atitikti tavo MySQL naudotoją, slaptažodį ir bazės pavadinimą.

---

### 3. Duomenų bazės paruošimas:

1. Įsitikink, kad veikia MySQL serveris.
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

Jei pavyko – nematysi klaidų, o duomenys bus matomi GUI ar CLI.

---

### 4. API paleidimas:

```bash
uvicorn app.main:app --reload
```

Swagger: http://localhost:8000/docs

---

## Darbo su šakomis eiga

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

`main` apsaugotas nuo tiesioginio push

---

## Naujo endpoint kūrimo gidas

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

2025
"# Autorent_api_google-github-login" 
