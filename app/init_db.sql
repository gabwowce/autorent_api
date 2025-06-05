-- ================================================
-- AUTORENTDB: MySQL duomenų bazės sukūrimo skriptas
-- ================================================

-- Sukuria duomenų bazę, jei tokios dar nėra, ir pasirenka ją naudojimui
CREATE DATABASE IF NOT EXISTS autorentdb;
USE autorentdb;

-- Sukuriama lentelė klientams saugoti
CREATE TABLE `Klientai` (
 `kliento_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
 `vardas` VARCHAR(255) NOT NULL,
 `pavarde` VARCHAR(255) NOT NULL,
 `el_pastas` VARCHAR(255) NOT NULL UNIQUE CHECK (`el_pastas` LIKE '%_@_%._%'),
 `telefono_nr` VARCHAR(255) NOT NULL,
 `gimimo_data` DATE NOT NULL,
 `registracijos_data` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 `bonus_taskai` INTEGER DEFAULT 0 CHECK (`bonus_taskai` >= 0)
);

-- Sukuriama lentelė automobilių nuomos užsakymams saugoti
CREATE TABLE `Uzsakymai` (
  `uzsakymo_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `kliento_id` INTEGER NOT NULL,
  `automobilio_id` INTEGER NOT NULL,
  `darbuotojo_id` INTEGER NOT NULL,
  `nuomos_data` DATE NOT NULL,
  `grazinimo_data` DATE NOT NULL,
  `paemimo_vietos_id` INTEGER NOT NULL,
  `grazinimo_vietos_id` INTEGER NOT NULL,
  `bendra_kaina` DECIMAL(10,2) NOT NULL,
  `uzsakymo_busena` ENUM('laukiama', 'patvirtinta', 'vykdoma', 'užbaigta', 'atšaukta') NOT NULL,
  `turi_papildomas_paslaugas` BOOLEAN NOT NULL DEFAULT FALSE
);

-- Sukuriama klientų užklausų ir palaikymo lentelė
CREATE TABLE `Klientu_Palaikymas` (
  `uzklausos_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `kliento_id` INTEGER NOT NULL,
  `darbuotojo_id` INTEGER, 
  `tema` VARCHAR(255) NOT NULL,
  `pranesimas` TEXT NOT NULL,
  `atsakymas` TEXT,
  `pateikimo_data` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  `atsakymo_data` TIMESTAMP
);

-- Sukuriama lentelė klientų atsiliepimams apie automobilius saugoti
CREATE TABLE `Automobilio_Atsiliepimai` (
  `atsiliepimo_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `kliento_id` INTEGER NOT NULL,
  `automobilio_id` INTEGER NOT NULL,
  `ivertinimas` INTEGER NOT NULL CHECK (`ivertinimas` BETWEEN 1 AND 5),
  `komentaras` TEXT,
  `data` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Sukuriama sąskaitų lentelė
CREATE TABLE `Saskaitos` (
  `saskaitos_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `uzsakymo_id` INTEGER NOT NULL,
  `suma` DECIMAL(10,2) NOT NULL,
  `saskaitos_data` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Sukuriama mokėjimų lentelė
CREATE TABLE `Mokejimai` (
  `mokejimo_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `uzsakymo_id` INTEGER NOT NULL,
  `suma` DECIMAL(10,2) NOT NULL,
  `mokejimo_data` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  `mokejimo_tipas`  ENUM('grynieji', 'kortele', 'bankinis pavedimas', 'paypal') NOT NULL
);

-- Sukuriama automobilių lentelė
CREATE TABLE `Automobiliai` (
  `automobilio_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `marke` VARCHAR(255) NOT NULL,
  `modelis` VARCHAR(255) NOT NULL,
  `metai` INTEGER NOT NULL,
  `numeris` VARCHAR(255) NOT NULL UNIQUE,
  `vin_kodas` VARCHAR(17) UNIQUE NOT NULL,
  `spalva` VARCHAR(255) NOT NULL,
  `kebulo_tipas` VARCHAR(255) NOT NULL,
  `pavarų_deze` ENUM('mechaninė', 'automatinė', 'pusiau automatinė') NOT NULL,
  `variklio_turis` DECIMAL(3,1) NOT NULL,
  `galia_kw` INTEGER NOT NULL,
  `kuro_tipas` ENUM('benzinas', 'dyzelinas', 'elektra', 'hibridas', 'dujos') NOT NULL,
  `rida` INTEGER NOT NULL,
  `sedimos_vietos` INTEGER NOT NULL,
  `klimato_kontrole` BOOLEAN NOT NULL DEFAULT FALSE,
  `navigacija` BOOLEAN NOT NULL DEFAULT FALSE,
  `kaina_parai` DECIMAL(10,2) NOT NULL,
  `automobilio_statusas` ENUM('laisvas', 'isnuomotas', 'servise', 'remonte') NOT NULL,
  `technikines_galiojimas` DATE NOT NULL,
  `dabartine_vieta_id` INTEGER NOT NULL,
  `pastabos` TEXT
);

-- Sukuriama lentelė automobilių aptarnavimo (serviso) darbams
CREATE TABLE `Automobiliu_Servisas` (
  `serviso_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `automobilio_id` INTEGER NOT NULL,
  `serviso_pradzios_data` DATE NOT NULL,
  `serviso_pabaigos_data` DATE,
  `plovimas` BOOLEAN NOT NULL DEFAULT FALSE,
  `salono_valymas` BOOLEAN NOT NULL DEFAULT FALSE,
  `technine_apziura` BOOLEAN NOT NULL DEFAULT FALSE,
  `tepalai_pakeisti` BOOLEAN NOT NULL DEFAULT FALSE,
  `kaina` DECIMAL(10,2) NOT NULL,
  `busena` ENUM('laukia', 'vyksta', 'baigtas') NOT NULL
);

-- Sukuriama kuro sąnaudų lentelė
CREATE TABLE `Kuro_Sanaudos` (
  `sanaudu_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `automobilio_id` INTEGER NOT NULL,
  `data` DATE NOT NULL,
  `kuro_kiekis` DECIMAL(10,2) NOT NULL,
  `kaina` DECIMAL(10,2) NOT NULL
);

-- Sukuriama remonto darbų lentelė
CREATE TABLE `Remonto_Darbai` (
  `remonto_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `automobilio_id` INTEGER NOT NULL,
  `remonto_pradzios_data` DATE NOT NULL,
  `remonto_pabaigos_data` DATE,
  `aprasymas` TEXT NOT NULL,
  `detales_pakeistos` TEXT,
  `garantija_menesiais` INTEGER,
  `meistras` VARCHAR(255) NOT NULL,
  `serviso_pavadinimas` VARCHAR(255) NOT NULL,
  `kaina` DECIMAL(10,2) NOT NULL,
  `busena` ENUM('laukia', 'vyksta', 'baigtas') NOT NULL
);

-- Sukuriama draudimų lentelė automobiliams
CREATE TABLE `Draudimai` (
  `draudimo_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `automobilio_id` INTEGER NOT NULL,
  `draudimo_tipas`  ENUM('civilinis', 'kasko', 'kita') NOT NULL,
  `galiojimo_pradzia` DATE NOT NULL,
  `galiojimo_pabaiga` DATE NOT NULL,
  `suma` DECIMAL(10,2) NOT NULL
);

-- Sukuriama baudų registravimo lentelė
CREATE TABLE `Baudu_Registras` (
  `baudos_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `automobilio_id` INTEGER NOT NULL,
  `baudos_priezastis` VARCHAR(255) NOT NULL,
  `data` DATE NOT NULL,
  `laikas` TIME NOT NULL DEFAULT '00:00:00',
  `suma` DECIMAL(10,2) NOT NULL,
  `kliento_id` INTEGER NOT NULL
);

-- Sukuriama darbuotojų lentelė
CREATE TABLE `Darbuotojai` (
 `darbuotojo_id` INTEGER PRIMARY key AUTO_INCREMENT,
 `vardas` VARCHAR(255) NOT NULL,
 `pavarde` VARCHAR(255) NOT NULL,
 `el_pastas` VARCHAR(255) NOT NULL UNIQUE CHECK (el_pastas LIKE '%_@_%._%'),
 `telefono_nr` VARCHAR(255) NOT NULL ,
 `pareigos` VARCHAR(255) NOT NULL,
 `atlyginimas` DECIMAL(10,2) NOT NULL,
 `isidarbinimo_data` DATE NOT NULL,
 `slaptazodis` VARCHAR(255) NOT NULL
);

-- Sukuriama lentelė atsakingiems darbuotojams už automobilius
CREATE TABLE `Atsakingi_Automobiliai` (
  `atsakomybes_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `darbuotojo_id` INTEGER NOT NULL,
  `automobilio_id` INTEGER NOT NULL,
  `pradzios_data` DATE NOT NULL,
  `pabaigos_data` DATE
);

-- Sukuriama papildomų paslaugų lentelė (pvz. vaikiška kėdutė, Wi-Fi ir pan.)
CREATE TABLE `Papildomos_Paslaugos` (
  `paslaugos_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `pavadinimas` VARCHAR(255) NOT NULL,
  `aprasymas` TEXT NOT NULL,
  `kaina` DECIMAL(10,2) NOT NULL
);

-- Sukuriama užsakymo-paslaugos jungiamoji lentelė
CREATE TABLE `Uzsakymo_Paslaugos` (
 `uzsakymo_paslaugos_id` INTEGER PRIMARY key AUTO_INCREMENT,
 `uzsakymo_id` INTEGER NOT NULL,
 `paslaugos_id` INTEGER NOT NULL
);

-- Sukuriama rezervacijų lentelė
CREATE TABLE `Rezervavimas` (
  `rezervacijos_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `kliento_id` INTEGER NOT NULL,
  `automobilio_id` INTEGER NOT NULL,
  `rezervacijos_pradzia` DATE NOT NULL,
  `rezervacijos_pabaiga` DATE NOT NULL,
  `busena` ENUM('patvirtinta', 'atšaukta', 'laukia') NOT NULL
);

-- Sukuriama nuolaidų lentelė
CREATE TABLE `Nuolaidos` (
 `nuolaidos_id` INTEGER PRIMARY key AUTO_INCREMENT,
 `pavadinimas` VARCHAR(255) NOT NULL,
 `procentas` DECIMAL(5,2) NOT NULL CHECK (`procentas` > 0 AND `procentas` <= 100),
 `galiojimo_pradzia` DATE NOT null, 
 `galiojimo_pabaiga` DATE NOT NULL 
);

-- Sukuriama jungiamoji lentelė užsakymo nuolaidoms
CREATE TABLE `Uzsakymo_Nuolaidos` (
  `uzsakymo_nuolaidos_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `uzsakymo_id` INTEGER NOT NULL,
  `nuolaidos_id` INTEGER NOT NULL
);

-- Sukuriama automobilių pristatymo ir grąžinimo vietų lentelė
CREATE TABLE `Pristatymo_Vietos` (
  `vietos_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `pavadinimas` VARCHAR(255) NOT NULL,
  `adresas` VARCHAR(255) NOT NULL ,
  `miestas` VARCHAR(255) NOT NULL 
);

-- Sukuriama automobilių kuro kortelių lentelė
CREATE TABLE `Kuro_Korteles` (
  `korteles_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `automobilio_id` INTEGER NOT NULL,
  `korteles_numeris` VARCHAR(255) UNIQUE NOT NULL,
  `galiojimo_pabaiga` DATE NOT NULL
);

-- Sukuriama lentelė bonusų naudojimui fiksuoti
CREATE TABLE `Bonusu_Naudojimas` (
  `naudojimo_id` INTEGER PRIMARY key AUTO_INCREMENT,
  `kliento_id` INTEGER NOT NULL,
  `uzsakymo_id` INTEGER NOT NULL,
  `panaudoti_taskai` INTEGER NOT NULL,
  `nuolaidos_id` INTEGER NOT NULL,
  `data` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Sukuriama lentelė automobilių grąžinimo vietoms saugoti
CREATE TABLE `Automobilio_Grazinimo_Vieta` (
  `grazinimo_vietos_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `automobilio_id` INTEGER NOT NULL,
  `vietos_id` INTEGER NOT NULL
);

-- Žemiau ALTER komandos, kurios prideda lentelių tarpusavio ryšius (užtikrina duomenų integralumą)
ALTER TABLE `Uzsakymai` ADD FOREIGN KEY (`kliento_id`) REFERENCES `Klientai` (`kliento_id`);
ALTER TABLE `Uzsakymai` ADD FOREIGN KEY (`darbuotojo_id`) REFERENCES `Darbuotojai` (`darbuotojo_id`);
ALTER TABLE `Klientu_Palaikymas` ADD FOREIGN KEY (`kliento_id`) REFERENCES `Klientai` (`kliento_id`);
ALTER TABLE `Automobilio_Atsiliepimai` ADD FOREIGN KEY (`kliento_id`) REFERENCES `Klientai` (`kliento_id`);
ALTER TABLE `Saskaitos` ADD FOREIGN KEY (`uzsakymo_id`) REFERENCES `Uzsakymai` (`uzsakymo_id`);
ALTER TABLE `Mokejimai` ADD FOREIGN KEY (`uzsakymo_id`) REFERENCES `Uzsakymai` (`uzsakymo_id`);
ALTER TABLE `Uzsakymai` ADD FOREIGN KEY (`paemimo_vietos_id`) REFERENCES `Pristatymo_Vietos` (`vietos_id`);
ALTER TABLE `Uzsakymai` ADD FOREIGN KEY (`grazinimo_vietos_id`) REFERENCES `Pristatymo_Vietos` (`vietos_id`);
ALTER TABLE `Automobilio_Atsiliepimai` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Uzsakymai` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Automobiliu_Servisas` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Kuro_Sanaudos` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Remonto_Darbai` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Draudimai` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Baudu_Registras` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Kuro_Korteles` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Atsakingi_Automobiliai` ADD FOREIGN KEY (`darbuotojo_id`) REFERENCES `Darbuotojai` (`darbuotojo_id`);
ALTER TABLE `Atsakingi_Automobiliai` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Uzsakymo_Paslaugos` ADD FOREIGN KEY (`uzsakymo_id`) REFERENCES `Uzsakymai` (`uzsakymo_id`);
ALTER TABLE `Uzsakymo_Paslaugos` ADD FOREIGN KEY (`paslaugos_id`) REFERENCES `Papildomos_Paslaugos` (`paslaugos_id`);
ALTER TABLE `Rezervavimas` ADD FOREIGN KEY (`kliento_id`) REFERENCES `Klientai` (`kliento_id`);
ALTER TABLE `Klientu_Palaikymas` ADD FOREIGN KEY (`darbuotojo_id`) REFERENCES `Darbuotojai` (`darbuotojo_id`);
ALTER TABLE `Rezervavimas` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Uzsakymo_Nuolaidos` ADD FOREIGN KEY (`uzsakymo_id`) REFERENCES `Uzsakymai` (`uzsakymo_id`);
ALTER TABLE `Uzsakymo_Nuolaidos` ADD FOREIGN KEY (`nuolaidos_id`) REFERENCES `Nuolaidos` (`nuolaidos_id`);
ALTER TABLE `Bonusu_Naudojimas` ADD FOREIGN KEY (`kliento_id`) REFERENCES `Klientai` (`kliento_id`);
ALTER TABLE `Bonusu_Naudojimas` ADD FOREIGN KEY (`uzsakymo_id`) REFERENCES `Uzsakymai` (`uzsakymo_id`);
ALTER TABLE `Bonusu_Naudojimas` ADD FOREIGN KEY (`nuolaidos_id`) REFERENCES `Nuolaidos` (`nuolaidos_id`);
ALTER TABLE `Automobiliai` ADD FOREIGN KEY (`dabartine_vieta_id`) REFERENCES `Pristatymo_Vietos` (`vietos_id`);
ALTER TABLE `Automobilio_Grazinimo_Vieta` ADD FOREIGN KEY (`automobilio_id`) REFERENCES `Automobiliai` (`automobilio_id`);
ALTER TABLE `Automobilio_Grazinimo_Vieta` ADD FOREIGN KEY (`vietos_id`) REFERENCES `Pristatymo_Vietos` (`vietos_id`);
ALTER TABLE `Baudu_Registras` ADD FOREIGN KEY (`kliento_id`) REFERENCES `Klientai` (`kliento_id`);

-- Žemiau prasideda pradinių duomenų įrašymas (insertai)

-- Pridedami klientų įrašai
INSERT INTO `Klientai` (`vardas`, `pavarde`, `el_pastas`, `telefono_nr`, `gimimo_data`, `registracijos_data`, `bonus_taskai`)
VALUES 
('Jonas', 'Petrauskas', 'jonas.petrauskas@example.com', '+37061234567', '1990-05-12', '2023-01-15 10:30:00', 150),
('Aistė', 'Kazlauskienė', 'aiste.kazlauskiene@example.com', '+37069876543', '1985-08-24', '2022-11-20 14:45:00', 200),
('Tomas', 'Vaitkus', 'tomas.vaitkus@example.com', '+37067788990', '1993-11-15', '2023-05-08 08:15:00', 50),
('Laura', 'Jankauskaitė', 'laura.jankauskaite@example.com', '+37064567890', '1988-02-10', '2021-07-01 12:00:00', 300),
('Paulius', 'Jonaitis', 'paulius.jonaitis@example.com', '+37060123456', '1995-07-30', '2022-09-10 17:30:00', 100),
('Gabija', 'Pakalniškytė', 'gabija.pakalniskyte@example.com', '+37061239876', '1992-03-21', '2023-03-18 09:20:00', 250),
('Mantas', 'Šimkus', 'mantas.simkus@example.com', '+37068991234', '1987-12-05', '2021-12-25 19:10:00', 400),
('Dovilė', 'Butkutė', 'dovile.butkute@example.com', '+37065432109', '1994-06-14', '2022-06-30 15:05:00', 175),
('Karolis', 'Rutkauskas', 'karolis.rutkauskas@example.com', '+37069987654', '1990-09-02', '2023-04-12 11:40:00', 50),
('Rasa', 'Grigaliūnaitė', 'rasa.grigaliunaite@example.com', '+37061122334', '1986-01-28', '2020-10-05 13:55:00', 225);

-- Įterpiami darbuotojų įrašai
INSERT INTO Darbuotojai (
    vardas, pavarde, el_pastas, telefono_nr, pareigos, atlyginimas, isidarbinimo_data, slaptazodis
) VALUES
('Tomas', 'Jonaitis', 'tomas.jonaitis@example.com', '+37060010001', 'Administratorius', 1800.00, '2022-05-10', '$2b$12$NVYVtCmorq1q8I4ME3Hly.d0XNYlKjhC3/XJVG/sPpyySjWDmBivy'),             -- "Slaptas123!"
('Rasa', 'Petrauskaitė', 'rasa.petrauskaite@example.com', '+37060010002', 'Vadybininkas', 1600.00, '2021-03-15', '$2b$12$0Bbtkv0fLnZ2Vs.q2K4wj.ObyzykJpYi7208Jr31BIhfa1p19eLZu'),           -- "ZaliaVarna1!"
('Mindaugas', 'Kazlauskas', 'mindaugas.kazlauskas@example.com', '+37060010003', 'Mechanikas', 1700.00, '2023-07-20', '$2b$12$fHaTKacMLvYAQU3LjlTlpOME9JkwRAOPmofoTner8LtiNIXXUF.wq'),       -- "Remontas#2024"
('Inga', 'Simonaitytė', 'inga.simonaityte@example.com', '+37060010004', 'Klientų aptarnavimas', 1500.00, '2020-09-10', '$2b$12$6EWWuMX.FE/rz/heYLcVhOFprPKFR3o4QFBhMAp/sWiofxdCRXxSC'),     -- "KavaSuPienu!"
('Saulius', 'Jankauskas', 'saulius.jankauskas@example.com', '+37060010005', 'Vadybininkas', 1650.00, '2019-12-01', '$2b$12$4d6Lb2GQOW2wX4Jiz2iopuLLZQ8C.ipR4Tfd.MHpdGUsj9PJ1J9u6'),         -- "Vadovas456@"
('Asta', 'Kudirkaitė', 'asta.kudirkaite@example.com', '+37060010006', 'Administratorius', 1750.00, '2021-06-18', '$2b$12$zJVlU7scuiaDZnfLC22e7eC5jRhhJjVA2jZGOIksCMGz3cuuqf06K'),           -- "ManoPaslaptis2$"
('Viktoras', 'Povilaitis', 'viktoras.povilaitis@example.com', '+37060010007', 'Mechanikas', 1800.00, '2022-11-05', '$2b$12$x4YR1TwjN1Xelx4ObxF7/uEs.MyHgXUGzBOTrrl0t53hbmCvr8yBO'),         -- "VerstaVariklis!"
('Simas', 'Urbonas', 'simas.urbonas@example.com', '+37060010008', 'Vadybininkas', 1550.00, '2020-04-25', '$2b$12$wxiOMo7808YHPprKXpBureS8pvPPaUszykl7B3IZ2H.ek3VKhvq5O'),                   -- "SimasPlius33#"
('Raimondas', 'Jasiūnas', 'raimondas.jasiunas@example.com', '+37060010009', 'Klientų aptarnavimas', 1450.00, '2018-08-30', '$2b$12$xpN9tIL.Df9w.tmekLfrXecf1Yjo4YOnzJubdDJ1DYdsvfooO0fQ.'), -- "Klientas2025@"
('Jolanta', 'Bagdonaitė', 'jolanta.bagdonaite@example.com', '+37060010010', 'Administratorius', 1600.00, '2023-01-12', '$2b$12$pVuQyfPH6Ee6Ytzejka8bub0wRIH3S353aIcflXGGJ9HJUtUpo5o.');     -- "SaugusKodas!"


-- Pridedamos pristatymo vietos
INSERT INTO `Pristatymo_Vietos` (`pavadinimas`, `adresas`, `miestas`)
VALUES
('Vilnius Centras', 'Gedimino pr. 1, Vilnius', 'Vilnius'),
('Kaunas Centras', 'Laisvės al. 10, Kaunas', 'Kaunas'),
('Klaipėda', 'Taikos pr. 20, Klaipėda', 'Klaipėda'),
('Šiauliai', 'Tilžės g. 5, Šiauliai', 'Šiauliai'),
('Panevėžys', 'Respublikos g. 15, Panevėžys', 'Panevėžys'),
('Alytus', 'Naujoji g. 30, Alytus', 'Alytus'),
('Marijampolė', 'Gedimino g. 5, Marijampolė', 'Marijampolė'),
('Utena', 'J. Basanavičiaus g. 3, Utena', 'Utena'),
('Mažeikiai', 'Laisvės g. 25, Mažeikiai', 'Mažeikiai'),
('Telšiai', 'Žemaitijos g. 7, Telšiai', 'Telšiai');

-- Pridedami automobilių įrašai
INSERT INTO Automobiliai (
   marke, modelis, metai, numeris, vin_kodas, spalva, kebulo_tipas, pavarų_deze,
   variklio_turis, galia_kw, kuro_tipas, rida, sedimos_vietos, klimato_kontrole,
   navigacija, kaina_parai, automobilio_statusas, technikines_galiojimas, dabartine_vieta_id, pastabos
) VALUES
('Toyota', 'Corolla', 2018, 'ABC123', 'JTDKB20U20345789', 'Sidabrinė', 'Sedanas', 'automatinė', 1.8, 90, 'hibridas', 85000, 5, TRUE, TRUE, 40.00, 'laisvas', '2025-06-15', 1, 'Puikus miesto automobilis'),
('Volkswagen', 'Golf', 2020, 'XYZ456', 'WVZZZ1KZAM124567', 'Juoda', 'Hečbekas', 'mechaninė', 2.0, 110, 'dyzelinas', 45000, 5, TRUE, TRUE, 50.00, 'isnuomotas', '2026-08-10', 2, NULL),
('BMW', 'X5', 2019, 'BMW789', 'WBABT52000D98765', 'Balta', 'Visureigis', 'automatinė', 3.0, 190, 'dyzelinas', 65000, 5, TRUE, TRUE, 80.00, 'laisvas', '2025-12-20', 3, 'Prabangus ir galingas'),
('Mercedes-Benz', 'E-Class', 2021, 'MB500', 'WDD210341A123987', 'Pilka', 'Sedanas', 'automatinė', 2.0, 150, 'benzinas', 35000, 5, TRUE, TRUE, 90.00, 'isnuomotas', '2027-03-10', 4, NULL),
('Audi', 'A4', 2017, 'AUD567', 'WAUZZZF47HA12654', 'Mėlyna', 'Sedanas', 'mechaninė', 1.8, 125, 'benzinas', 120000, 5, TRUE, FALSE, 45.00, 'laisvas', '2024-09-25', 5, 'Ekonomiškas pasirinkimas'),
('Ford', 'Focus', 2016, 'FOR888', 'WF05XXGCC5GG23123', 'Raudona', 'Hečbekas', 'mechaninė', 1.6, 85, 'benzinas', 98000, 5, FALSE, FALSE, 35.00, 'laisvas', '2024-12-10', 6, NULL),
('Tesla', 'Model 3', 2022, 'TES999', '5YJ3E1EA7J123321', 'Balta', 'Sedanas', 'automatinė', 0.0, 283, 'elektra', 25000, 5, TRUE, TRUE, 100.00, 'isnuomotas', '2027-07-05', 7, 'Naujausias modelis su autopilotu'),
('Honda', 'Civic', 2015, 'HON333', 'JHMFC1550F123890', 'Sidabrinė', 'Sedanas', 'mechaninė', 1.5, 88, 'benzinas', 140000, 5, FALSE, FALSE, 30.00, 'servise', '2024-06-30', 8, 'Reikalingas smulkus remontas'),
('Nissan', 'Qashqai', 2018, 'NIS666', 'SJNFAAJ11U236547', 'Juoda', 'Visureigis', 'pusiau automatinė', 1.6, 96, 'benzinas', 78000, 5, TRUE, TRUE, 55.00, 'laisvas', '2025-11-15', 9, NULL),
('Skoda', 'Superb', 2020, 'SKD777', 'TMBJJ9NP2L128765', 'Žalia', 'Sedanas', 'automatinė', 2.0, 140, 'dyzelinas', 41000, 5, TRUE, TRUE, 60.00, 'laisvas', '2026-05-30', 10, 'Talpus ir komfortiškas');

-- Pridedamos papildomos paslaugos
INSERT INTO `Papildomos_Paslaugos` (
    `pavadinimas`, `aprasymas`, `kaina`
) VALUES
('Vaikiška kėdutė', 'Saugos kėdutė vaikams nuo 9 mėn. iki 12 metų.', 5.00),
('GPS navigacija', 'Naujausia GPS sistema su atnaujintais žemėlapiais.', 7.00),
('Papildomas vairuotojas', 'Galimybė registruoti antrą vairuotoją prie nuomos sutarties.', 10.00),
('Pilnas draudimas', 'Pilnas draudimas, padengiantis visus galimus nuostolius.', 20.00),
('Stogo bagažinė', 'Papildoma vieta bagažui kelionėms su daugiau daiktų.', 8.00),
('Wi-Fi modemas', 'Mobilus Wi-Fi interneto ryšys automobilyje (neriboti duomenys).', 6.50),
('Žiemos paketas', 'Žieminės padangos, langų skystis ir grandinės slidžioms sąlygoms.', 12.00),
('Automobilio pristatymas', 'Automobilio pristatymas į pasirinktą vietą nuomos pradžiai.', 15.00),
('Automobilio grąžinimas kitoje vietoje', 'Galimybė grąžinti automobilį kitoje vietoje nei paėmimo vieta.', 25.00),
('Kuro paslauga', 'Pilnas kuro bakas nuomos pradžioje su galimybe grąžinti tuščią.', 30.00);

-- Pridedami nuolaidų įrašai
INSERT INTO `Nuolaidos` (
    `pavadinimas`, `procentas`, `galiojimo_pradzia`, `galiojimo_pabaiga`
) VALUES
('Pavasario akcija', 10.00, '2025-03-01', '2025-03-31'),
('Lojalaus kliento nuolaida', 15.00, '2025-01-01', '2025-12-31'),
('Vasaros specialus pasiūlymas', 12.50, '2025-06-01', '2025-08-31'),
('Savaitgalio nuolaida', 5.00, '2025-02-01', '2025-02-28'),
('Ilgalaikės nuomos nuolaida', 20.00, '2025-01-01', '2025-12-31'),
('Kalėdinė akcija', 25.00, '2025-12-01', '2025-12-31'),
('Naujoko nuolaida', 8.00, '2025-04-01', '2025-06-30'),
('Rudens pasiūlymas', 10.00, '2025-09-01', '2025-10-31'),
('Juodojo penktadienio nuolaida', 30.00, '2025-11-29', '2025-11-30'),
('Gimtadienio nuolaida', 18.00, '2025-01-01', '2025-12-31');

-- Įterpiami užsakymų įrašai
INSERT INTO `Uzsakymai` (
    `kliento_id`, `automobilio_id`, `darbuotojo_id`, `nuomos_data`,
    `grazinimo_data`, `paemimo_vietos_id`, `grazinimo_vietos_id`,
    `bendra_kaina`, `uzsakymo_busena`, `turi_papildomas_paslaugas`
) VALUES
(1, 1, 2, '2025-02-01', '2025-02-05', 1, 2, 150.00, 'patvirtinta', TRUE),
(2, 2, 4, '2025-02-02', '2025-02-07', 2, 3, 220.00, 'vykdoma', FALSE),
(3, 3, 1, '2025-02-03', '2025-02-06', 3, 1, 180.00, 'užbaigta', TRUE),
(4, 4, 5, '2025-02-04', '2025-02-10', 1, 4, 300.00, 'atšaukta', FALSE),
(5, 5, 3, '2025-02-05', '2025-02-09', 4, 2, 200.00, 'patvirtinta', TRUE),
(6, 6, 2, '2025-02-06', '2025-02-12', 3, 5, 250.00, 'laukiama', FALSE),
(7, 7, 4, '2025-02-07', '2025-02-11', 5, 1, 270.00, 'vykdoma', TRUE),
(8, 8, 6, '2025-02-08', '2025-02-13', 2, 4, 350.00, 'užbaigta', FALSE),
(9, 9, 7, '2025-02-09', '2025-02-14', 4, 3, 400.00, 'patvirtinta', TRUE),
(10, 10, 8, '2025-02-10', '2025-02-15', 1, 5, 500.00, 'laukiama', FALSE);

-- Įterpiami sąskaitų įrašai
INSERT INTO `Saskaitos` (`uzsakymo_id`, `suma`, `saskaitos_data`)
VALUES
(1, 150.00, '2025-02-05 13:00:00'),
(2, 220.00, '2025-02-08 11:30:00'),
(3, 180.00, '2025-02-07 16:45:00'),
(4, 300.00, '2025-02-11 09:15:00'),
(5, 200.00, '2025-02-10 17:20:00'),
(6, 250.00, '2025-02-13 12:10:00'),
(7, 270.00, '2025-02-12 08:45:00'),
(8, 350.00, '2025-02-14 19:05:00'),
(9, 400.00, '2025-02-15 10:55:00'),
(10, 500.00, '2025-02-16 14:40:00');

-- Įterpiami mokėjimų įrašai
INSERT INTO `Mokejimai` (`uzsakymo_id`, `suma`, `mokejimo_tipas`)
VALUES 
(1, 150.00, 'kortele'),
(2, 220.00, 'bankinis pavedimas'),
(3, 180.00, 'grynieji'),
(4, 300.00, 'paypal'),
(5, 200.00, 'kortele'),
(6, 250.00, 'grynieji'),
(7, 270.00, 'kortele'),
(8, 350.00, 'bankinis pavedimas'),
(9, 400.00, 'kortele'),
(10, 500.00, 'grynieji');

-- Įterpiami atsakingų darbuotojų už automobilius įrašai
INSERT INTO `Atsakingi_Automobiliai` (
    `darbuotojo_id`, `automobilio_id`, `pradzios_data`, `pabaigos_data`
) VALUES
(1, 1, '2024-01-10', '2024-06-15'),
(2, 2, '2023-12-05', '2024-05-20'),
(3, 3, '2024-02-01', NULL),         -- Vis dar atsakingas
(4, 4, '2023-11-20', '2024-04-10'),
(5, 5, '2024-03-01', NULL),         -- Vis dar atsakingas
(6, 6, '2023-10-15', '2024-02-28'),
(7, 7, '2024-01-25', NULL),         -- Vis dar atsakingas
(8, 8, '2023-09-05', '2024-03-12'),
(9, 9, '2024-02-10', NULL),         -- Vis dar atsakingas
(10, 10, '2023-08-01', '2024-01-31');

-- Įterpiami klientų palaikymo įrašai
INSERT INTO `Klientu_Palaikymas` (
    `kliento_id`, `darbuotojo_id`, `tema`, `pranesimas`, `atsakymas`, `pateikimo_data`, `atsakymo_data`
) VALUES
(1, 3, 'Automobilio gedimas', 'Automobilis pradėjo skleisti keistus garsus važiuojant.', 'Jūsų automobilis buvo patikrintas, ir nustatyta, kad tai smulki techninė problema. Remontas atliktas.', '2025-02-20 10:15:00', '2025-02-21 14:30:00'),
(2, NULL, 'Rezervacijos atšaukimas', 'Noriu atšaukti savo užsakymą, nes planai pasikeitė.', NULL, '2025-02-21 12:00:00', NULL),
(3, 5, 'Kainos klausimas', 'Ar galiu gauti nuolaidą ilgalaikei nuomai?', 'Taip, ilgalaikėms nuomoms taikomos specialios nuolaidos. Susisiekite dėl išsamesnės informacijos.', '2025-02-22 09:45:00', '2025-02-22 16:00:00'),
(4, NULL, 'Pamiršau daiktą automobilyje', 'Palikau telefoną nuomotame automobilyje. Kaip galėčiau jį atsiimti?', NULL, '2025-02-23 14:20:00', NULL),
(5, 7, 'Sąskaitos klausimas', 'Kodėl mano sąskaitoje rodoma papildoma suma?', 'Papildoma suma priskaičiuota už degalų trūkumą grąžinant automobilį.', '2025-02-24 08:10:00', '2025-02-24 12:40:00'),
(6, 2, 'Automobilio keitimas', 'Ar galiu pakeisti rezervuotą automobilį į kitą modelį?', 'Taip, galima pakeisti automobilį, jei yra laisvų modelių. Prašome susisiekti.', '2025-02-25 11:30:00', '2025-02-25 17:15:00'),
(7, NULL, 'Techninė problema', 'Negaliu prisijungti prie savo paskyros jūsų svetainėje.', NULL, '2025-02-26 15:50:00', NULL),
(8, 4, 'Apmokėjimo klausimas', 'Ar galiu sumokėti grynaisiais, kai atsiimsiu automobilį?', 'Taip, priimame ir grynųjų pinigų mokėjimus atsiimant automobilį.', '2025-02-27 13:10:00', '2025-02-27 16:45:00'),
(9, 6, 'Papildomos paslaugos', 'Ar galima užsisakyti vaikišką kėdutę kartu su automobiliu?', 'Taip, už papildomą mokestį galima pridėti vaikišką kėdutę prie rezervacijos.', '2025-02-28 09:00:00', '2025-02-28 12:20:00'),
(10, NULL, 'Skundas dėl aptarnavimo', 'Buvau nepatenkintas darbuotojo bendravimu nuomos punkte.', NULL, '2025-02-28 18:30:00', NULL);

-- Įterpiami automobilių atsiliepimų įrašai
INSERT INTO `Automobilio_Atsiliepimai` (
  `kliento_id`, `automobilio_id`, `ivertinimas`, `komentaras`, `data`
) VALUES
(1, 1, 5, 'Labai patogus ir ekonomiškas automobilis. Važiavau ilgą kelionę – jokių problemų.', '2025-02-15 10:30:00'),
(2, 2, 4, 'Automobilis buvo tvarkingas, bet salone jautėsi kvapas.', '2025-02-16 14:20:00'),
(3, 3, 3, 'Vidutinė patirtis – automobilis veikė gerai, bet turėjo keletą įbrėžimų.', '2025-02-17 12:45:00'),
(4, 4, 5, 'Puikus pasirinkimas – patogus, ekonomiškas ir gerai prižiūrėtas.', '2025-02-18 08:55:00'),
(5, 5, 2, 'Automobilis buvo nešvarus, o stabdžiai atrodė susidėvėję.', '2025-02-19 18:40:00'),
(6, 6, 4, 'Labai malonu vairuoti, bet navigacija buvo pasenusi.', '2025-02-20 09:15:00'),
(7, 7, 5, 'Viskas tobula – užsakysiu vėl!', '2025-02-21 16:00:00'),
(8, 8, 3, 'Automobilis buvo patogus, bet kuro sąnaudos buvo didesnės nei tikėjausi.', '2025-02-22 11:30:00'),
(9, 9, 1, 'Prasta patirtis – automobilis turėjo mechaninių problemų.', '2025-02-23 20:10:00'),
(10, 10, 4, 'Geras automobilis, bet kaina galėtų būti mažesnė.', '2025-02-24 13:45:00');

-- Įterpiami automobilių serviso darbų įrašai
INSERT INTO `Automobiliu_Servisas` (
    `automobilio_id`, `serviso_pradzios_data`, `serviso_pabaigos_data`, 
    `plovimas`, `salono_valymas`, `technine_apziura`, `tepalai_pakeisti`, 
    `kaina`, `busena`
) VALUES
(1, '2025-02-01', '2025-02-02', TRUE, TRUE, FALSE, TRUE, 120.00, 'baigtas'),
(2, '2025-02-05', '2025-02-06', TRUE, FALSE, TRUE, TRUE, 250.00, 'baigtas'),
(3, '2025-02-10', NULL, FALSE, FALSE, TRUE, FALSE, 80.00, 'vyksta'),
(4, '2025-02-12', '2025-02-14', TRUE, TRUE, FALSE, FALSE, 150.00, 'baigtas'),
(5, '2025-02-15', NULL, FALSE, TRUE, TRUE, TRUE, 300.00, 'vyksta'),
(6, '2025-02-18', '2025-02-19', TRUE, FALSE, FALSE, TRUE, 100.00, 'baigtas'),
(7, '2025-02-20', '2025-02-21', FALSE, FALSE, TRUE, TRUE, 200.00, 'baigtas'),
(8, '2025-02-22', NULL, TRUE, TRUE, FALSE, FALSE, 180.00, 'vyksta'),
(9, '2025-02-24', NULL, FALSE, TRUE, TRUE, TRUE, 320.00, 'laukia'),
(10, '2025-02-26', '2025-02-27', TRUE, TRUE, FALSE, TRUE, 140.00, 'baigtas');

-- Įterpiami kuro sąnaudų įrašai
INSERT INTO `Kuro_Sanaudos` (
    `automobilio_id`, `data`, `kuro_kiekis`, `kaina`
) VALUES
(1, '2025-02-01', 45.50, 90.00),
(2, '2025-02-02', 50.00, 100.00),
(3, '2025-02-03', 30.25, 60.50),
(4, '2025-02-04', 40.75, 85.00),
(5, '2025-02-05', 55.00, 110.00),
(6, '2025-02-06', 42.30, 84.60),
(7, '2025-02-07', 35.75, 71.50),
(8, '2025-02-08', 60.00, 120.00),
(9, '2025-02-09', 38.50, 77.00),
(10, '2025-02-10', 44.10, 88.20);

-- Pridedami remonto darbai
INSERT INTO `Remonto_Darbai` (
    `automobilio_id`, `remonto_pradzios_data`, `remonto_pabaigos_data`,
    `aprasymas`, `detales_pakeistos`, `garantija_menesiais`, `meistras`,
    `serviso_pavadinimas`, `kaina`, `busena`
) VALUES
(1, '2025-02-01', '2025-02-03', 'Variklio remontas', 'Paskirstymo diržas, vandens pompa', 12, 'Tomas Kazlauskas', 'AutoFix Servisas', 450.00, 'baigtas'),
(2, '2025-02-05', '2025-02-07', 'Stabdžių sistemos keitimas', 'Stabdžių diskai ir kaladėlės', 6, 'Rimas Jonaitis', 'Fast Auto', 320.00, 'baigtas'),
(3, '2025-02-10', NULL, 'Kėbulo dažymas', NULL, NULL, 'Lukas Petrauskas', 'ColorCar', 600.00, 'vyksta'),
(4, '2025-02-12', '2025-02-14', 'Sankabos keitimas', 'Sankabos komplektas', 24, 'Marius Žilinskas', 'Top Repair', 750.00, 'baigtas'),
(5, '2025-02-15', NULL, 'Elektrinės sistemos remontas', 'Akumuliatorius, laidai', 6, 'Dovydas Stankevičius', 'ElectroFix', 280.00, 'vyksta'),
(6, '2025-02-18', '2025-02-19', 'Kondicionieriaus remontas', 'Kompresorius', 12, 'Aurimas Vaitkus', 'CoolCar Servisas', 200.00, 'baigtas'),
(7, '2025-02-20', '2025-02-21', 'Pakabos remontas', 'Amortizatoriai, stabilizatoriai', 18, 'Andrius Vilkas', 'Suspension Masters', 500.00, 'baigtas'),
(8, '2025-02-22', NULL, 'Starterio remontas', 'Starteris', 12, 'Gintaras Lekavičius', 'Quick Fix', 350.00, 'vyksta'),
(9, '2025-02-24', NULL, 'Turbinos remontas', 'Turbina, vamzdynai', 12, 'Vaidotas Šimkus', 'Turbo Pro', 680.00, 'laukia'),
(10, '2025-02-26', '2025-02-27', 'Duslintuvo keitimas', 'Duslintuvas', 6, 'Julius Jankauskas', 'Exhaust Experts', 250.00, 'baigtas');

-- Pridedami draudimų įrašai
INSERT INTO `Draudimai` (
    `automobilio_id`, `draudimo_tipas`, `galiojimo_pradzia`, `galiojimo_pabaiga`, `suma`
) VALUES
(1, 'civilinis', '2025-01-01', '2025-12-31', 120.00),
(2, 'kasko', '2025-02-01', '2026-01-31', 450.00),
(3, 'civilinis', '2025-03-01', '2026-02-28', 130.00),
(4, 'kasko', '2025-04-01', '2026-03-31', 500.00),
(5, 'civilinis', '2025-05-01', '2026-04-30', 140.00),
(6, 'kasko', '2025-06-01', '2026-05-31', 470.00),
(7, 'civilinis', '2025-07-01', '2026-06-30', 125.00),
(8, 'kasko', '2025-08-01', '2026-07-31', 480.00),
(9, 'civilinis', '2025-09-01', '2026-08-31', 135.00),
(10, 'kita', '2025-10-01', '2026-09-30', 300.00);

-- Pridedami baudų registro įrašai
INSERT INTO `Baudu_Registras` (
    `automobilio_id`, `baudos_priezastis`, `data`, `suma`, `kliento_id`
) VALUES
(1, 'Greičio viršijimas (+20 km/h)', '2025-02-01', 50.00, 3),
(2, 'Neleistinas parkavimas', '2025-02-05', 30.00, 5),
(3, 'Važiavimas be saugos diržo', '2025-02-07', 20.00, 2),
(4, 'Raudono šviesoforo nepaisymas', '2025-02-10', 100.00, 7),
(5, 'Netinkama eismo juosta', '2025-02-12', 25.00, 1),
(6, 'Greičio viršijimas (+30 km/h)', '2025-02-15', 80.00, 4),
(7, 'Automobilio palikimas ant žalios vejos', '2025-02-18', 40.00, 8),
(8, 'Važiavimas be techninės apžiūros', '2025-02-20', 120.00, 6),
(9, 'Neapmokėtas mokamas kelias', '2025-02-22', 15.00, 9),
(10, 'Parkavimas neįgaliųjų vietoje', '2025-02-25', 150.00, 10),
(1, 'Telefono naudojimas vairuojant', '2025-02-26', 35.00, 3),
(3, 'Neįjungti žibintai dienos metu', '2025-02-28', 10.00, 2),
(5, 'Važiavimas dviračių taku', '2025-03-01', 70.00, 1),
(7, 'Netinkamas lenkimas', '2025-03-03', 90.00, 8),
(9, 'Krovinio svorio viršijimas', '2025-03-05', 200.00, 9);

-- Pridedami užsakymo-paslaugų ryšiai
INSERT INTO `Uzsakymo_Paslaugos` (`uzsakymo_id`, `paslaugos_id`) VALUES
(1, 1),  -- Vaikiška kėdutė
(1, 4),  -- Pilnas draudimas
(3, 2),  -- GPS navigacija
(3, 5),  -- Stogo bagažinė
(5, 3),  -- Papildomas vairuotojas
(5, 6),  -- Wi-Fi modemas
(7, 7),  -- Žiemos paketas
(7, 8),  -- Automobilio pristatymas
(9, 9),  -- Automobilio grąžinimas kitoje vietoje
(9, 10); -- Kuro paslauga

-- Pridedami rezervacijų įrašai
INSERT INTO `Rezervavimas` (
    `kliento_id`, `automobilio_id`, `rezervacijos_pradzia`, `rezervacijos_pabaiga`, `busena`
) VALUES
(1, 1, '2025-03-01', '2025-03-05', 'patvirtinta'),
(2, 2, '2025-03-02', '2025-03-07', 'laukia'),
(3, 3, '2025-03-03', '2025-03-06', 'patvirtinta'),
(4, 4, '2025-03-04', '2025-03-10', 'atšaukta'),
(5, 5, '2025-03-05', '2025-03-09', 'patvirtinta'),
(6, 6, '2025-03-06', '2025-03-12', 'laukia'),
(7, 7, '2025-03-07', '2025-03-11', 'patvirtinta'),
(8, 8, '2025-03-08', '2025-03-13', 'atšaukta'),
(9, 9, '2025-03-09', '2025-03-14', 'patvirtinta'),
(10, 10, '2025-03-10', '2025-03-15', 'laukia');

-- Pridedami užsakymo-nuolaidų ryšiai
INSERT INTO `Uzsakymo_Nuolaidos` (`uzsakymo_id`, `nuolaidos_id`) VALUES
(1, 2), -- Lojalaus kliento nuolaida
(2, 5), -- Ilgalaikės nuomos nuolaida
(3, 7), -- Naujoko nuolaida
(4, 1), -- Pavasario akcija
(5, 10); -- Gimtadienio nuolaida

-- Pridedamos kuro kortelės
INSERT INTO `Kuro_Korteles` (`automobilio_id`, `korteles_numeris`, `galiojimo_pabaiga`)
VALUES
(1, 'FK-001-2025', '2026-02-28'),
(2, 'FK-002-2025', '2026-03-15'),
(3, 'FK-003-2025', '2026-04-10'),
(4, 'FK-004-2025', '2026-05-05'),
(5, 'FK-005-2025', '2026-06-20'),
(6, 'FK-006-2025', '2026-07-30'),
(7, 'FK-007-2025', '2026-08-25'),
(8, 'FK-008-2025', '2026-09-15'),
(9, 'FK-009-2025', '2026-10-10'),
(10, 'FK-010-2025', '2026-11-05');

-- Pridedamas bonusų naudojimas
INSERT INTO `Bonusu_Naudojimas` (
    `kliento_id`, `uzsakymo_id`, `panaudoti_taskai`, `nuolaidos_id`, `data`
) VALUES
(1, 1, 150, 2, '2025-02-05 12:00:00'),  -- Lojalaus kliento nuolaida
(3, 2, 200, 5, '2025-02-10 14:30:00'),  -- Ilgalaikės nuomos nuolaida
(5, 3, 100, 7, '2025-02-15 16:45:00'),  -- Naujoko nuolaida
(7, 4, 250, 1, '2025-02-20 10:15:00'),  -- Pavasario akcija
(9, 5, 300, 10, '2025-02-25 18:00:00'); -- Gimtadienio nuolaida

-- Pridedamos automobilio grąžinimo vietos
INSERT INTO `Automobilio_Grazinimo_Vieta` (
    `automobilio_id`, `vietos_id`
) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 1),
(7, 2),
(8, 3),
(9, 4),
(10, 5);


-- ====================================================================
--                    'Delete' endpointų tvarkymas
-- ====================================================================

-- 1. Pirma reikia paruošti stulpelius (jei jie turi būti NULLABLE):
ALTER TABLE Uzsakymai MODIFY darbuotojo_id INTEGER NULL;
ALTER TABLE Uzsakymai MODIFY kliento_id INTEGER NULL;
ALTER TABLE Uzsakymai MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Uzsakymai MODIFY paemimo_vietos_id INTEGER NULL;
ALTER TABLE Uzsakymai MODIFY grazinimo_vietos_id INTEGER NULL;
ALTER TABLE Klientu_Palaikymas MODIFY kliento_id INTEGER NULL;
ALTER TABLE Klientu_Palaikymas MODIFY darbuotojo_id INTEGER NULL;
ALTER TABLE Automobilio_Atsiliepimai MODIFY kliento_id INTEGER NULL;
ALTER TABLE Automobilio_Atsiliepimai MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Saskaitos MODIFY uzsakymo_id INTEGER NULL;
ALTER TABLE Mokejimai MODIFY uzsakymo_id INTEGER NULL;
ALTER TABLE Atsakingi_Automobiliai MODIFY darbuotojo_id INTEGER NULL;
ALTER TABLE Atsakingi_Automobiliai MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Uzsakymo_Paslaugos MODIFY uzsakymo_id INTEGER NULL;
ALTER TABLE Uzsakymo_Paslaugos MODIFY paslaugos_id INTEGER NULL;
ALTER TABLE Rezervavimas MODIFY kliento_id INTEGER NULL;
ALTER TABLE Rezervavimas MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Uzsakymo_Nuolaidos MODIFY uzsakymo_id INTEGER NULL;
ALTER TABLE Uzsakymo_Nuolaidos MODIFY nuolaidos_id INTEGER NULL;
ALTER TABLE Bonusu_Naudojimas MODIFY kliento_id INTEGER NULL;
ALTER TABLE Bonusu_Naudojimas MODIFY uzsakymo_id INTEGER NULL;
ALTER TABLE Bonusu_Naudojimas MODIFY nuolaidos_id INTEGER NULL;
ALTER TABLE Automobiliai MODIFY dabartine_vieta_id INTEGER NULL;
ALTER TABLE Automobilio_Grazinimo_Vieta MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Automobilio_Grazinimo_Vieta MODIFY vietos_id INTEGER NULL;
ALTER TABLE Kuro_Korteles MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Kuro_Sanaudos MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Automobiliu_Servisas MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Remonto_Darbai MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Draudimai MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Baudu_Registras MODIFY automobilio_id INTEGER NULL;
ALTER TABLE Baudu_Registras MODIFY kliento_id INTEGER NULL;

-- 2. Dabar keičiam užsienio raktus (pradžioje reikia ištrinti senus):

-- Trinam visus užsienio raktų apribojimus
ALTER TABLE Uzsakymai DROP FOREIGN KEY Uzsakymai_ibfk_1;
ALTER TABLE Uzsakymai DROP FOREIGN KEY Uzsakymai_ibfk_2;
ALTER TABLE Uzsakymai DROP FOREIGN KEY Uzsakymai_ibfk_3;
ALTER TABLE Uzsakymai DROP FOREIGN KEY Uzsakymai_ibfk_4;
ALTER TABLE Uzsakymai DROP FOREIGN KEY Uzsakymai_ibfk_5;
ALTER TABLE Uzsakymai DROP FOREIGN KEY Uzsakymai_ibfk_6;

ALTER TABLE Klientu_Palaikymas DROP FOREIGN KEY Klientu_Palaikymas_ibfk_1;
ALTER TABLE Klientu_Palaikymas DROP FOREIGN KEY Klientu_Palaikymas_ibfk_2;

ALTER TABLE Automobilio_Atsiliepimai DROP FOREIGN KEY Automobilio_Atsiliepimai_ibfk_1;
ALTER TABLE Automobilio_Atsiliepimai DROP FOREIGN KEY Automobilio_Atsiliepimai_ibfk_2;

ALTER TABLE Saskaitos DROP FOREIGN KEY Saskaitos_ibfk_1;
ALTER TABLE Mokejimai DROP FOREIGN KEY Mokejimai_ibfk_1;

ALTER TABLE Atsakingi_Automobiliai DROP FOREIGN KEY Atsakingi_Automobiliai_ibfk_1;
ALTER TABLE Atsakingi_Automobiliai DROP FOREIGN KEY Atsakingi_Automobiliai_ibfk_2;

ALTER TABLE Uzsakymo_Paslaugos DROP FOREIGN KEY Uzsakymo_Paslaugos_ibfk_1;
ALTER TABLE Uzsakymo_Paslaugos DROP FOREIGN KEY Uzsakymo_Paslaugos_ibfk_2;

ALTER TABLE Rezervavimas DROP FOREIGN KEY Rezervavimas_ibfk_1;
ALTER TABLE Rezervavimas DROP FOREIGN KEY Rezervavimas_ibfk_2;

ALTER TABLE Uzsakymo_Nuolaidos DROP FOREIGN KEY Uzsakymo_Nuolaidos_ibfk_1;
ALTER TABLE Uzsakymo_Nuolaidos DROP FOREIGN KEY Uzsakymo_Nuolaidos_ibfk_2;

ALTER TABLE Bonusu_Naudojimas DROP FOREIGN KEY Bonusu_Naudojimas_ibfk_1;
ALTER TABLE Bonusu_Naudojimas DROP FOREIGN KEY Bonusu_Naudojimas_ibfk_2;
ALTER TABLE Bonusu_Naudojimas DROP FOREIGN KEY Bonusu_Naudojimas_ibfk_3;

ALTER TABLE Automobiliai DROP FOREIGN KEY Automobiliai_ibfk_1;

ALTER TABLE Automobilio_Grazinimo_Vieta DROP FOREIGN KEY Automobilio_Grazinimo_Vieta_ibfk_1;
ALTER TABLE Automobilio_Grazinimo_Vieta DROP FOREIGN KEY Automobilio_Grazinimo_Vieta_ibfk_2;

ALTER TABLE Kuro_Korteles DROP FOREIGN KEY Kuro_Korteles_ibfk_1;
ALTER TABLE Kuro_Sanaudos DROP FOREIGN KEY Kuro_Sanaudos_ibfk_1;
ALTER TABLE Automobiliu_Servisas DROP FOREIGN KEY Automobiliu_Servisas_ibfk_1;
ALTER TABLE Remonto_Darbai DROP FOREIGN KEY Remonto_Darbai_ibfk_1;
ALTER TABLE Draudimai DROP FOREIGN KEY Draudimai_ibfk_1;
ALTER TABLE Baudu_Registras DROP FOREIGN KEY Baudu_Registras_ibfk_1;
ALTER TABLE Baudu_Registras DROP FOREIGN KEY Baudu_Registras_ibfk_2;

-- Sukuriam iš naujo su ON DELETE SET NULL
ALTER TABLE Uzsakymai ADD CONSTRAINT fk_uzsakymai_klientas FOREIGN KEY (kliento_id) REFERENCES Klientai(kliento_id) ON DELETE SET NULL;
ALTER TABLE Uzsakymai ADD CONSTRAINT fk_uzsakymai_darbuotojas FOREIGN KEY (darbuotojo_id) REFERENCES Darbuotojai(darbuotojo_id) ON DELETE SET NULL;
ALTER TABLE Uzsakymai ADD CONSTRAINT fk_uzsakymai_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;
ALTER TABLE Uzsakymai ADD CONSTRAINT fk_uzsakymai_paemimo_vieta FOREIGN KEY (paemimo_vietos_id) REFERENCES Pristatymo_Vietos(vietos_id) ON DELETE SET NULL;
ALTER TABLE Uzsakymai ADD CONSTRAINT fk_uzsakymai_grazinimo_vieta FOREIGN KEY (grazinimo_vietos_id) REFERENCES Pristatymo_Vietos(vietos_id) ON DELETE SET NULL;

ALTER TABLE Klientu_Palaikymas ADD CONSTRAINT fk_palaikymas_klientas FOREIGN KEY (kliento_id) REFERENCES Klientai(kliento_id) ON DELETE SET NULL;
ALTER TABLE Klientu_Palaikymas ADD CONSTRAINT fk_palaikymas_darbuotojas FOREIGN KEY (darbuotojo_id) REFERENCES Darbuotojai(darbuotojo_id) ON DELETE SET NULL;

ALTER TABLE Automobilio_Atsiliepimai ADD CONSTRAINT fk_atsiliepimai_klientas FOREIGN KEY (kliento_id) REFERENCES Klientai(kliento_id) ON DELETE SET NULL;
ALTER TABLE Automobilio_Atsiliepimai ADD CONSTRAINT fk_atsiliepimai_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;

ALTER TABLE Saskaitos ADD CONSTRAINT fk_saskaitos_uzsakymas FOREIGN KEY (uzsakymo_id) REFERENCES Uzsakymai(uzsakymo_id) ON DELETE SET NULL;
ALTER TABLE Mokejimai ADD CONSTRAINT fk_mokejimai_uzsakymas FOREIGN KEY (uzsakymo_id) REFERENCES Uzsakymai(uzsakymo_id) ON DELETE SET NULL;

ALTER TABLE Atsakingi_Automobiliai ADD CONSTRAINT fk_atsakingi_darbuotojas FOREIGN KEY (darbuotojo_id) REFERENCES Darbuotojai(darbuotojo_id) ON DELETE SET NULL;
ALTER TABLE Atsakingi_Automobiliai ADD CONSTRAINT fk_atsakingi_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;

ALTER TABLE Uzsakymo_Paslaugos ADD CONSTRAINT fk_uzsakymo_paslaugos_uzsakymas FOREIGN KEY (uzsakymo_id) REFERENCES Uzsakymai(uzsakymo_id) ON DELETE SET NULL;
ALTER TABLE Uzsakymo_Paslaugos ADD CONSTRAINT fk_uzsakymo_paslaugos_paslauga FOREIGN KEY (paslaugos_id) REFERENCES Papildomos_Paslaugos(paslaugos_id) ON DELETE SET NULL;

ALTER TABLE Rezervavimas ADD CONSTRAINT fk_rezervavimas_klientas FOREIGN KEY (kliento_id) REFERENCES Klientai(kliento_id) ON DELETE SET NULL;
ALTER TABLE Rezervavimas ADD CONSTRAINT fk_rezervavimas_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;

ALTER TABLE Uzsakymo_Nuolaidos ADD CONSTRAINT fk_uzsakymo_nuolaidos_uzsakymas FOREIGN KEY (uzsakymo_id) REFERENCES Uzsakymai(uzsakymo_id) ON DELETE SET NULL;
ALTER TABLE Uzsakymo_Nuolaidos ADD CONSTRAINT fk_uzsakymo_nuolaidos_nuolaida FOREIGN KEY (nuolaidos_id) REFERENCES Nuolaidos(nuolaidos_id) ON DELETE SET NULL;

ALTER TABLE Bonusu_Naudojimas ADD CONSTRAINT fk_bonusu_klientas FOREIGN KEY (kliento_id) REFERENCES Klientai(kliento_id) ON DELETE SET NULL;
ALTER TABLE Bonusu_Naudojimas ADD CONSTRAINT fk_bonusu_uzsakymas FOREIGN KEY (uzsakymo_id) REFERENCES Uzsakymai(uzsakymo_id) ON DELETE SET NULL;
ALTER TABLE Bonusu_Naudojimas ADD CONSTRAINT fk_bonusu_nuolaida FOREIGN KEY (nuolaidos_id) REFERENCES Nuolaidos(nuolaidos_id) ON DELETE SET NULL;

ALTER TABLE Automobiliai ADD CONSTRAINT fk_automobiliai_vieta FOREIGN KEY (dabartine_vieta_id) REFERENCES Pristatymo_Vietos(vietos_id) ON DELETE SET NULL;

ALTER TABLE Automobilio_Grazinimo_Vieta ADD CONSTRAINT fk_grazinimo_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;
ALTER TABLE Automobilio_Grazinimo_Vieta ADD CONSTRAINT fk_grazinimo_vieta FOREIGN KEY (vietos_id) REFERENCES Pristatymo_Vietos(vietos_id) ON DELETE SET NULL;

ALTER TABLE Kuro_Korteles ADD CONSTRAINT fk_kuro_korteles_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;
ALTER TABLE Kuro_Sanaudos ADD CONSTRAINT fk_kuro_sanaudos_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;
ALTER TABLE Automobiliu_Servisas ADD CONSTRAINT fk_servisas_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;
ALTER TABLE Remonto_Darbai ADD CONSTRAINT fk_remontas_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;
ALTER TABLE Draudimai ADD CONSTRAINT fk_draudimai_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;
ALTER TABLE Baudu_Registras ADD CONSTRAINT fk_baudos_automobilis FOREIGN KEY (automobilio_id) REFERENCES Automobiliai(automobilio_id) ON DELETE SET NULL;
ALTER TABLE Baudu_Registras ADD CONSTRAINT fk_baudos_klientas FOREIGN KEY (kliento_id) REFERENCES Klientai(kliento_id) ON DELETE SET NULL;

-- ====================================================================
--                              PASTABA
-- ====================================================================

-- Užsienio raktų pavadinimai (ibfk_1, ibfk_2 ir t.t.) priklauso nuo MySQL versijos ir kaip jie buvo sugeneruoti
-- jei pavadinimai neatitinka, reikia patikrinti su SHOW CREATE TABLE ir pakeisti pagal faktinius raktus.
