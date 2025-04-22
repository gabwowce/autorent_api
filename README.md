# 🚗 Car Rental System API

Projektas skirtas **vidinei darbuotojų automobilių nuomos sistemos valdymo** daliai. Backend sukurtas su **FastAPI**, naudojant **JWT autentifikaciją** ir aiškiai struktūruotą sluoksninę architektūrą.

---

## ♻️ Architektūra (Layered Structure)

```
POST /api/v1/auth/login
    │
    ▼
[ endpoint (auth.py) ]
    │
    ├➞ schemas/ ➞ validacija (LoginRequest)
    ├➞ repositories/ ➞ DB užklausos (get_by_email)
    └➞ services/ ➞ verslo logika (slaptažodžių tikrinimas, JWT)
```

---

## 📂 Kodo struktūra

```
autorent_api/
├── app/
│   ├── main.py                       ➞ Programos paleidimo failas
│   ├── api/
│   │   └── v1/endpoints/
│   │       ├── auth.py              ➞ Prisijungimas / registracija
│   │       ├── employee.py          ➞ Darbuotojų CRUD
│   │       └── car.py               ➞ Automobilių CRUD
│   ├── db/
│   │   ├── session.py               ➞ DB sesija
│   │   └── base.py                  ➞ Modelių registracija
│   ├── models/                      ➞ SQLAlchemy modeliai
│   │   ├── employee.py
│   │   └── car.py
│   ├── schemas/                     ➞ Pydantic input/output schemos
│   │   ├── auth.py
│   │   ├── employee.py
│   │   └── car.py
│   ├── repositories/                ➞ DB logika
│   │   └── employee.py, car.py
│   ├── services/                    ➞ Verslo logika
│   │   └── auth_service.py
│   └── api/deps.py                  ➞ priklausomybių injekcija
├── init_db.sql                      ➞ Duomenų bazės struktūra + pradiniai duomenys
├── .env.example                     ➞ Pavyzdinis konfigūracijos failas
└── requirements.txt
```

---

## 🔐 Autentifikacija

- JWT tokenas generuojamas per `POST /api/v1/auth/login`
- `get_current_user()` tikrina tokeną visiems apsaugotiems endpointams

**Endpointai:**

- [`POST /api/v1/auth/login`](http://localhost:8000/docs#/Authentication/login_api_v1_auth_login_post)
- [`POST /api/v1/auth/register`](http://localhost:8000/docs#/Authentication/register_api_v1_auth_register_post)
- [`GET /api/v1/auth/me`](http://localhost:8000/docs#/Authentication/me_api_v1_auth_me_get)

---

## 💼 Darbuotojai

CRUD veiksmai:

- Gauti visus darbuotojus (viešas)
- Redaguoti / Ištrinti darbuotoją

**Failai:** `schemas/employee.py`, `repositories/employee.py`, `endpoints/employee.py`

---

## 🚗 Automobiliai

Pilnas CRUD + būsenos keitimas:

- Pridėti, redaguoti, pašalinti
- `PATCH /cars/{id}/status`

**Failai:** `schemas/car.py`, `repositories/car.py`, `endpoints/car.py`

---

## ⚙️ Projekto paleidimo instrukcija komandai

### 1. Klonavimas ir priklausomybės:

```bash
git clone https://github.com/TAVO-VARDAS/autorent_api.git
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

📅 README atnaujinta: 2025-04-22
