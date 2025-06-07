# 🚀 API Endpointų Planas

Projektas: **Automobilių nuomos sistema**

Šis dokumentas aprašo visus realiai įgyvendintus REST API endpointus, kurie naudojami sistemoje. Visi endpointai suskirstyti pagal logines sekcijas.

---

## 🔐 1. Autentifikacija (`/auth`)

| Endpoint           | Metodas | Aprašymas                                   |
|--------------------|---------|---------------------------------------------|
| `/login`           | POST    | Prisijungimas, grąžina JWT                  |
| `/logout`          | POST    | Atsijungimas (tokenas šalinamas kliento pusėje) |
| `/register`        | POST    | Darbuotojo registracija                     |
| `/me`              | GET     | Prisijungusio darbuotojo info               |
| `/change-password` | POST    | Pakeisti slaptažodį                         |

---

## 👨‍💼 2. Darbuotojai (`/employees`)

| Endpoint  | Metodas | Aprašymas                          |
|-----------|---------|------------------------------------|
| `/`       | GET     | Gauti visus darbuotojus            |
| `/{id}`   | GET     | Gauti vieną darbuotoją pagal ID    |
| `/`       | POST    | Sukurti naują darbuotoją           |
| `/{id}`   | PUT     | Atnaujinti darbuotojo info         |
| `/{id}`   | DELETE  | Pašalinti darbuotoją               |

---

## 👤 3. Klientai (`/clients`)

| Endpoint            | Metodas | Aprašymas                                |
|---------------------|---------|------------------------------------------|
| `/`                 | GET     | Gauti visus klientus                     |
| `/{id}`             | GET     | Gauti vieną klientą pagal ID             |
| `/`                 | POST    | Sukurti naują klientą                    |
| `/{id}`             | PUT     | Atnaujinti kliento info                  |
| `/{id}`             | DELETE  | Pašalinti klientą                        |
| `/{id}/orders`      | GET     | Kliento užsakymai                        |

---

## 🚗 4. Automobiliai (`/cars`)

| Endpoint         | Metodas | Aprašymas                       |
|------------------|---------|---------------------------------|
| `/`              | GET     | Gauti visus automobilius        |
| `/{id}`          | GET     | Vienas automobilis pagal ID     |
| `/`              | POST    | Pridėti naują automobilį        |
| `/{id}`          | PUT     | Atnaujinti automobilio duomenis |
| `/{id}`          | DELETE  | Pašalinti automobilį            |
| `/{id}/status`   | PATCH   | Pakeisti automobilio būseną     |
| `/search`        | GET     | Paieška/filtravimas pagal laukus|

---

## 💼 5. Užsakymai (`/orders`)

| Endpoint                   | Metodas | Aprašymas                      |
|----------------------------|---------|--------------------------------|
| `/`                        | GET     | Visi užsakymai                 |
| `/{id}`                    | GET     | Vienas užsakymas               |
| `/`                        | POST    | Naujas užsakymas               |
| `/{id}`                    | PUT     | Atnaujinti užsakymą            |
| `/{id}`                    | DELETE  | Ištrinti/atšaukti užsakymą     |
| `/by-client/{kliento_id}`  | GET     | Visi kliento užsakymai         |
| `/stats/by-status`         | GET     | Užsakymų statistika pagal būseną |

---

## 📑 6. Sąskaitos (`/invoices`)

| Endpoint              | Metodas | Aprašymas                       |
|-----------------------|---------|---------------------------------|
| `/`                   | GET     | Visos sąskaitos                 |
| `/`                   | POST    | Nauja sąskaita                  |
| `/{id}`               | DELETE  | Pašalinti sąskaitą              |
| `/{id}/status`        | PATCH   | Pakeisti sąskaitos statusą      |

---

## 💬 7. Klientų aptarnavimas (`/support`)

| Endpoint              | Metodas | Aprašymas                             |
|-----------------------|---------|---------------------------------------|
| `/`                   | GET     | Visos klientų užklausos               |
| `/`                   | POST    | Nauja užklausa                        |
| `/unanswered`         | GET     | Neatsakytos užklausos                 |
| `/{id}`               | GET     | Viena užklausa                        |
| `/{id}`               | PATCH   | Atsakyti/atnaujinti užklausą          |
| `/{id}`               | DELETE  | Pašalinti užklausą                    |

---

## 🚊 8. Rezervacijos (`/reservations`)

| Endpoint         | Metodas | Aprašymas                          |
|------------------|---------|------------------------------------|
| `/`              | GET     | Visos rezervacijos                 |
| `/latest`        | GET     | Naujausios rezervacijos            |
| `/{id}`          | GET     | Viena rezervacija pagal ID         |
| `/`              | POST    | Nauja rezervacija                  |
| `/{id}`          | PUT     | Atnaujinti rezervaciją             |
| `/{id}`          | DELETE  | Ištrinti rezervaciją               |
| `/search`        | GET     | Paieška pagal filtrus              |

---

## 🗺️ 9. Geokodavimas (`/geocode`)

| Endpoint    | Metodas | Aprašymas                                  |
|-------------|---------|--------------------------------------------|
| `/geocode`  | POST    | Adreso geokodavimas (lat/lng pagal adresą) |

---

**PASTABA:**  
- Visi endpoint’ai grąžina duomenis su HATEOAS nuorodomis.  
- Visi svarbiausi veiksmai testuoti su Swagger bei Postman.

---

