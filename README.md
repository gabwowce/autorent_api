# Car Rental System API

Projektas skirtas **vidinei darbuotojų automobilių nuomos sistemos valdymo** daliai. Backend sukurtas su **FastAPI**, naudojant **JWT autentifikaciją** ir aiškiai struktūruotą sluoksninę architektūrą.

---

## Architektūra (Layered Structure)

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

## Kodo struktūra

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
└── requirements.txt
```

---

## Autentifikacija

- JWT tokenas generuojamas per `POST /api/v1/auth/login`
- `get_current_user()` tikrina tokeną visiems apsaugotiems endpointams

**Endpointai:**
- [`POST /api/v1/auth/login`](http://localhost:8000/docs#/Authentication/login_api_v1_auth_login_post)
- [`POST /api/v1/auth/register`](http://localhost:8000/docs#/Authentication/register_api_v1_auth_register_post)
- [`GET /api/v1/auth/me`](http://localhost:8000/docs#/Authentication/me_api_v1_auth_me_get)

---

## Darbuotojai

CRUD veiksmai:
- Gauti visus darbuotojus (viešas)
- Redaguoti / Ištrinti darbuotoją

**Failai:** `schemas/employee.py`, `repositories/employee.py`, `endpoints/employee.py`

**Swagger:**
- [`GET /api/v1/employees/`](http://localhost:8000/docs#/Employees/get_employees_api_v1_employees__get)

---

## Automobiliai

Pilnas CRUD + būsenos keitimas:
- Pridėti, redaguoti, pašalinti
- `PATCH /cars/{id}/status`

**Failai:** `schemas/car.py`, `repositories/car.py`, `endpoints/car.py`

**Swagger:**
- [`GET /api/v1/cars/`](http://localhost:8000/docs#/Cars/get_all_cars_api_v1_cars__get)
- [`POST /api/v1/cars/`](http://localhost:8000/docs#/Cars/create_car_api_v1_cars__post)

---

## Projekto naudojimas komandai

### 1. Projekto paleidimas

```bash
git clone https://github.com/TAVO-VARDAS/autorent_api.git
cd autorent_api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Savo šakos (branch) sukūrimas

Kiekvienas narys turi dirbti savo šakoje pagal funkcionalumą. Šakos pavadinimo formatas:
```
feature/<funkcionalumas>  pvz:  feature/orders-endpoints
fix/<problema>            pvz:  fix/login-validation
```

#### Komandos pavyzdys:
```bash
git checkout -b feature/orders-endpoints
git add .
git commit -m "Sukurtas orders CRUD"
git push origin feature/orders-endpoints
```

---

## Kaip kurti naujus endpointus (struktūruotai)

1. **Sukurk SQLAlchemy modelį**
   - `models/<modulis>.py`
2. **Sukurk schemas** (įėjimo/išėjimo)
   - `schemas/<modulis>.py` su `ModelCreate`, `ModelUpdate`, `ModelOut`
3. **Sukurk duomenų prieigos logiką**
   - `repositories/<modulis>.py` su `get_all`, `get_by_id`, `create`, `update`, `delete`
4. **Sukurk endpoint failą**
   - `api/v1/endpoints/<modulis>.py` su FastAPI router'iu
5. **Registruok router'į į `main.py`**:
   ```python
   from app.api.v1.endpoints import <modulis>
   app.include_router(<modulis>.router, prefix="/api/v1/<modulis>", tags=["<Modulis>"])
   ```
6. **Swagger'e testuok veikimą:** [`http://localhost:8000/docs`](http://localhost:8000/docs)

---
