# 🚀 API Endpointų Planas

Projektas: **Automobilių nuomos sistema**

Šis dokumentas nurodo visus suplanuotus REST API endpointus, kurie bus naudojami projektuojant ir kuriant sistemą. Endpointai suskirstyti pagal logines sekcijas.

---

## 🔐 1. Autentifikacija (`/auth`)

| Endpoint    | Metodas | Aprašymas                                       |
| ----------- | ------- | ----------------------------------------------- |
| `/login`    | POST    | Prisijungimas, grąžina JWT                      |
| `/logout`   | POST    | Atsijungimas (tokenas šalinamas kliento pusėje) |
| `/register` | POST    | Darbuotojo registracija (admin)                 |
| `/me`       | GET     | Prisijungusio darbuotojo info                   |

---

## 👨‍💼 2. Darbuotojai (`/employees`)

| Endpoint | Metodas | Aprašymas                                  |
| -------- | ------- | ------------------------------------------ |
| `/`      | GET     | Gauti visus darbuotojus                    |
| `/{id}`  | GET     | Gauti vieną darbuotoją pagal ID            |
| `/{id}`  | PUT     | Atnaujinti darbuotojo info (role, tel. nr) |
| `/{id}`  | DELETE  | Pašalinti darbuotoją                       |

---

## 🚗 3. Automobiliai (`/cars`)

| Endpoint       | Metodas | Aprašymas                       |
| -------------- | ------- | ------------------------------- |
| `/`            | GET     | Gauti visus automobilius        |
| `/{id}`        | GET     | Vienas automobilis pagal ID     |
| `/`            | POST    | Pridėti naują automobilį        |
| `/{id}`        | PUT     | Atnaujinti automobilio duomenis |
| `/{id}`        | DELETE  | Pašalinti automobilį            |
| `/{id}/status` | PATCH   | Pakeisti automobilio būseną     |

---

## 💼 4. Užsakymai (`/orders`)

| Endpoint | Metodas | Aprašymas           |
| -------- | ------- | ------------------- |
| `/`      | GET     | Visi užsakymai      |
| `/{id}`  | GET     | Vienas užsakymas    |
| `/`      | POST    | Naujas užsakymas    |
| `/{id}`  | PUT     | Atnaujinti užsakymą |
| `/{id}`  | DELETE  | Atšaukti užsakymą   |

---

## 📃 5. Sąskaitos ir mokėjimai (`/invoices`, `/payments`)

| Endpoint     | Metodas | Aprašymas        |
| ------------ | ------- | ---------------- |
| `/invoices/` | GET     | Visos sąskaitos  |
| `/payments/` | GET     | Visi mokėjimai   |
| `/payments/` | POST    | Naujas mokėjimas |

---

## 💬 6. Klientų palaikymas (`/support`)

| Endpoint      | Metodas | Aprašymas               |
| ------------- | ------- | ----------------------- |
| `/`           | GET     | Visos klientų užklausos |
| `/`           | POST    | Nauja užklausa          |
| `/{id}/reply` | PUT     | Atsakyti į užklausą     |

---

## ⭐ 7. Atsiliepimai (`/reviews`)

| Endpoint | Metodas | Aprašymas            |
| -------- | ------- | -------------------- |
| `/`      | GET     | Visi atsiliepimai    |
| `/`      | POST    | Naujas atsiliepimas  |
| `/{id}`  | DELETE  | Ištrinti atsiliepimą |

---

## ⚙️ 8. Servisas ir remontas (`/service`, `/repair`)

| Endpoint    | Metodas | Aprašymas             |
| ----------- | ------- | --------------------- |
| `/service/` | GET     | Serviso įrašai        |
| `/service/` | POST    | Naujas serviso įrašas |
| `/repair/`  | GET     | Remonto įrašai        |
| `/repair/`  | POST    | Naujas remonto įrašas |

---

## 🚊 9. Rezervacijos (`/reservations`)

| Endpoint | Metodas | Aprašymas              |
| -------- | ------- | ---------------------- |
| `/`      | GET     | Visos rezervacijos     |
| `/`      | POST    | Nauja rezervacija      |
| `/{id}`  | PUT     | Atnaujinti rezervaciją |
| `/{id}`  | DELETE  | Atšaukti rezervaciją   |

---

## 💲 10. Paslaugos, nuolaidos, bonusai

| Endpoint       | Metodas  | Aprašymas               |
| -------------- | -------- | ----------------------- |
| `/services/`   | GET/POST | Papildomų paslaugų CRUD |
| `/discounts/`  | GET/POST | Nuolaidų valdymas       |
| `/bonuses/`    | GET      | Kliento bonusų peržiūra |
| `/bonuses/use` | POST     | Naudoti bonusus         |

---
