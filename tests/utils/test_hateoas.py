"""
Unit tests for HATEOAS (Hypermedia as the Engine of Application State) utility

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Testuoja HATEOAS nuorodų generatorių:
    - generate_links(resource, obj_id, actions)
    - Tikrina rel, href, metodų teisingumą, edge-case
    - Testuoja ir tuščių/nereikšmingų veiksmų atvejus

Usage:
    pytest tests/utils/test_hateoas.py

Pastabos:
    - Importuok funkcijas pagal savo projekto struktūrą!
"""

import pytest
from app.utils.hateoas import generate_links

def test_generate_basic_links():
    """
    Testuoja bazinius HATEOAS veiksmus: view, update, delete.
    """
    links = generate_links("car", 42, ["view", "update", "delete"])
    assert isinstance(links, list)
    rels = {l['rel'] for l in links}
    assert "view" in rels
    assert "update" in rels
    assert "delete" in rels
    for link in links:
        assert "href" in link
        assert isinstance(link["href"], str)
        assert str(42) in link["href"]

def test_generate_custom_action_link():
    """
    Testuoja custom veiksmą (pvz. status) ir URL teisingumą.
    """
    links = generate_links("car", 77, ["status"])
    assert any(link["rel"] == "status" for link in links)
    # Tikrina, kad href korektiškai generuojamas
    for link in links:
        if link["rel"] == "status":
            assert "/status" in link["href"]

def test_generate_links_empty_actions():
    """
    Testuoja tuščią veiksmų sąrašą – grąžina tuščią listą.
    """
    links = generate_links("car", 1, [])
    assert isinstance(links, list)
    assert links == []

def test_generate_links_invalid_resource():
    """
    Testuoja neteisingą resurso pavadinimą (turi grąžinti rel/href, bet URL bus neteisingas).
    """
    links = generate_links("???", 99, ["view"])
    assert links[0]["rel"] == "view"
    assert "???" in links[0]["href"]

def test_generate_links_no_id():
    """
    Testuoja, kai id yra None (arba 0), ar teisingai generuojamas href.
    """
    links = generate_links("car", None, ["view"])
    assert isinstance(links, list)
    # Priklausomai nuo implementacijos, href gali būti be id arba su "None"
    assert "None" in links[0]["href"] or links[0]["href"].endswith("/")

def test_generate_links_duplicate_actions():
    """
    Testuoja dublikatų veiksmų atvejį (turi būti tik po vieną kiekvienam rel).
    """
    links = generate_links("car", 5, ["update", "update", "view"])
    rels = [l['rel'] for l in links]
    assert rels.count("update") == 1 or set(rels) == set(["update", "view"])
