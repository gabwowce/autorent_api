"""
Repository tests for Car (Automobiliai)

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Unit testai automobilių repository sluoksniui (CRUD metodai):
    - create_car, get_car_by_id, update_car, delete_car, get_all_cars
    - Edge-case: neegzistuojantis įrašas, trūkstami laukai
    - Visi testai rollback'inami (nepalieka duomenų DB)

Usage:
    pytest tests/repositories/test_car.py

Reikalavimai:
    - conftest.py aprašytas db_session fixture (rollback po kiekvieno testavimo)
    - Reali repository sluoksnio funkcijų implementacija (pvz., CarRepository)
"""

import pytest

# Pvz., taip (adaptuok pagal savo projektą):
# from app.repositories.car import CarRepository
# from app.models import Car
# from app.schemas import CarCreate, CarUpdate

# Dummy duomenys
CAR_SAMPLE = {
    "marke": "Mazda",
    "modelis": "CX-5",
    "metai": 2023,
    "numeris": "TEST-REPO-1",
    "vin_kodas": "JH4TB2H26CC000001",
    "spalva": "Raudona",
    "kebulo_tipas": "Visureigis",
    "pavarų_deze": "Automatinė",
    "variklio_turis": 2.2,
    "galia_kw": 110,
    "kuro_tipas": "Dyzelinas",
    "rida": 21000,
    "sedimos_vietos": 5,
    "klimato_kontrole": True,
    "navigacija": True,
    "kaina_parai": 65.0,
    "automobilio_statusas": "laisvas",
    "technikines_galiojimas": "2026-12-31",
    "dabartine_vieta_id": None,
    "pastabos": "Test repository"
}

@pytest.fixture
def sample_car_data():
    """Grąžina naujo automobilio duomenų kopiją."""
    return CAR_SAMPLE.copy()

def test_create_car(db_session, sample_car_data):
    """
    Testuoja automobilio sukūrimą per repository.
    """
    # Adaptuok pagal savo repository klasę/funkciją!
    car = CarRepository.create_car(db_session, sample_car_data)
    assert car is not None
    assert car.marke == sample_car_data["marke"]
    assert car.automobilio_id is not None

def test_get_car_by_id_success(db_session, sample_car_data):
    """
    Testuoja automobilio gavimą pagal ID (sėkmė).
    """
    car = CarRepository.create_car(db_session, sample_car_data)
    found = CarRepository.get_car_by_id(db_session, car.automobilio_id)
    assert found is not None
    assert found.automobilio_id == car.automobilio_id
    assert found.modelis == car.modelis

def test_get_car_by_id_not_found(db_session):
    """
    Testuoja automobilio gavimą pagal neegzistuojantį ID (turi būti None arba exception).
    """
    found = CarRepository.get_car_by_id(db_session, 999999)
    assert found is None  # arba assert su exception, jei taip implementuota

def test_update_car_success(db_session, sample_car_data):
    """
    Testuoja automobilio atnaujinimą (PUT per repo).
    """
    car = CarRepository.create_car(db_session, sample_car_data)
    update_data = {"marke": "Peugeot", "modelis": "3008"}
    updated = CarRepository.update_car(db_session, car.automobilio_id, update_data)
    assert updated.marke == "Peugeot"
    assert updated.modelis == "3008"
    assert updated.automobilio_id == car.automobilio_id

def test_update_car_not_found(db_session):
    """
    Testuoja automobilio atnaujinimą neegzistuojančiam ID (turi būti None arba exception).
    """
    update_data = {"marke": "Fake"}
    updated = CarRepository.update_car(db_session, 999999, update_data)
    assert updated is None  # arba assert su exception

def test_delete_car_success(db_session, sample_car_data):
    """
    Testuoja automobilio ištrynimą (delete per repo).
    """
    car = CarRepository.create_car(db_session, sample_car_data)
    result = CarRepository.delete_car(db_session, car.automobilio_id)
    assert result is True
    # Įsitikina, kad automobilio nebėra
    found = CarRepository.get_car_by_id(db_session, car.automobilio_id)
    assert found is None

def test_delete_car_not_found(db_session):
    """
    Testuoja automobilio trynimą neegzistuojančiam ID (turi būti False arba exception).
    """
    result = CarRepository.delete_car(db_session, 999999)
    assert result is False  # arba assert su exception

def test_get_all_cars(db_session, sample_car_data):
    """
    Testuoja visų automobilių gavimą (bent 1 turi būti DB po create).
    """
    car = CarRepository.create_car(db_session, sample_car_data)
    cars = CarRepository.get_all_cars(db_session)
    assert isinstance(cars, list)
    assert any(c.automobilio_id == car.automobilio_id for c in cars)
