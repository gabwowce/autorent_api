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
│   │       └── car.py              ➞ Automobilių CRUD
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
│   └── api/deps.py                 ➞ priklausomybių injekcija
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

**Swagger:**

- [`GET /api/v1/employees/`](http://localhost:8000/docs#/Employees/get_employees_api_v1_employees__get)

---

## 🚗 Automobiliai

Pilnas CRUD + būsenos keitimas:

- Pridėti, redaguoti, pašalinti
- `PATCH /cars/{id}/status`

**Failai:** `schemas/car.py`, `repositories/car.py`, `endpoints/car.py`

**Swagger:**

- [`GET /api/v1/cars/`](http://localhost:8000/docs#/Cars/get_all_cars_api_v1_cars__get)
- [`POST /api/v1/cars/`](http://localhost:8000/docs#/Cars/create_car_api_v1_cars__post)

---

## ⚙️ Projekto paleidimo instrukcija komandai

### 1. Klonavimas ir priklausomybės:

```bash
git clone https://github.com/TAVO-VARDAS/autorent_api.git
cd autorent_api
pip install -r requirements.txt
```

### 2. `.env` failo paruošimas:

1. Terminale įvesk:

```bash
cp .env.example .env
```

Tai sukurs `.env` failą pagal pavyzdinį `.env.example`.

2. Atidaryk failą `.env` savo redaktoriuje (VS Code ar Notepad):

3. Rask eilutę, kuri prasideda:

```
DATABASE_URL=
```

4. Ir pakeisk ją į:

```
DATABASE_URL=mysql+pymysql://root:12301@localhost:3306/autorentdb
```

Tai reiškia, kad prisijungimas prie tavo lokalios MySQL bazės vyks su naudotoju `root`, slaptažodžiu `12301` ir naudojama `autorentdb` duomenų bazė.

📌 Jei tavo MySQL prisijungimo duomenys kitokie – atitinkamai pakeisk naudotoją, slaptažodį ar duomenų bazės pavadinimą.bash
cp .env.example .env

```
🔧 Tada atsidaryk `.env` ir pakeisk prisijungimą prie DB:
```

DATABASE_URL=mysql+pymysql://root:12301@localhost:3306/autorentdb

````

### 3. Duomenų bazės paruošimas:

1. Įsitikink, kad veikia MySQL serveris. Tai gali būti:
   - 🟢 **XAMPP** (dažniausias variantas Windows naudotojams)
   - 🟢 **MAMP** (dažnai naudojamas macOS)
   - 🟢 **WAMP** (kitas lokalus MySQL variantas)
   - 🟢 **MySQL kaip atskiras įdiegimas** (per `mysql-installer`)
   - 🟢 **MySQL Workbench** (GUI administravimui)
   - 🟢 **DBeaver** (kelių DB GUI, labai patogus)
   - 🟢 **phpMyAdmin** (naršyklėje veikiantis įrankis per XAMPP)

2. Sukurk duomenų bazę naudodamas bet kurį iš aukščiau pateiktų įrankių:
   - Per terminalą:
```sql
CREATE DATABASE autorentdb;
````

- Arba tiesiog GUI įrankyje paspausk "New database" ir sukurk `autorentdb`

3. Įrašyk struktūrą ir testinius duomenis:

```bash
mysql -u root -p autorentdb < init_db.sql
```

🟡 Kur:

- `-u root` – tavo MySQL naudotojo vardas (jei nenaudoji root, įrašyk savąjį)
- `-p` – MySQL paprašys slaptažodžio (pvz.: `12301`)
- `autorentdb` – turi atitikti tavo `.env` esantį `DATABASE_URL`

✅ Jei viskas pavyko – pamatysi "Query OK", "Records inserted" arba jokių klaidų.

````


---

### 4. API paleidimas:
```bash
uvicorn app.main:app --reload
````

📜 Swagger dokumentacija → http://localhost:8000/docs

---

## 👥 Darbo su šakomis eiga

### 1. Naujos šakos kūrimas:

```bash
git checkout -b feature/orders-endpoints
```

### 2. Įkėlimas į GitHub:

```bash
git add .
git commit -m "Sukurtas orders CRUD"
git push origin feature/orders-endpoints
```

> Visi nariai dirba tik savo šakose. `main` apsaugotas nuo tiesioginio `push`.

### 3. Pull request:

1. Eik į GitHub repo → tavo šaka
2. Spausk **„Compare & pull request“**
3. Patvirtink ir **merge** (jei leidžiama)

---

## 🧱 Naujo endpoint kūrimo gidas

1. `models/` ➞ SQLAlchemy modelis
2. `schemas/` ➞ `ModelCreate`, `ModelUpdate`, `ModelOut`
3. `repositories/` ➞ CRUD funkcijos
4. `endpoints/` ➞ FastAPI router su route'ais
5. `main.py` ➞ pridėti router:

```python
from app.api.v1.endpoints import orders
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
```

6. Swagger testavimas: [http://localhost:8000/docs](http://localhost:8000/docs)

---

✅ Jei viską padarei teisingai – turėsi pilnai veikiančią sistemą su testiniais duomenimis.

🛠️ Jei reikia pagalbos – kreipkis į projekto architektą!

---
