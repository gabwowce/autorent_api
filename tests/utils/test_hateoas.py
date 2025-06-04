"""
Unit tests for the HATEOAS (Hypermedia as the Engine of Application State) utility.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Tests the HATEOAS link generator utility:
    - generate_links(resource, obj_id, actions)
    - Verifies correctness of rel, href, and supported actions.
    - Checks edge cases and handling of empty or unusual actions.

Usage:
    Run tests using:
        pytest tests/utils/test_hateoas.py

Notes:
    - Make sure to import functions according to your project structure!
"""

import pytest
from utils.hateoas import generate_links

def test_generate_basic_links():
    """
    Tests that generate_links returns the expected basic links
    for 'view' (should be 'self'), 'update', and 'delete' actions.
    Asserts all expected relations are present in the generated links.
    """
    links = generate_links("car", 42, ["view", "update", "delete"])
    rels = {l['rel'] for l in links}
    assert "self" in rels
    assert "update" in rels
    assert "delete" in rels

def test_generate_custom_action_link():
    """
    Tests that generate_links correctly handles a custom action ('update_status').
    Asserts that the relation is present and the href contains '/status'.
    """
    links = generate_links("car", 77, ["update_status"])
    assert any(link["rel"] == "update_status" for link in links)
    for link in links:
        if link["rel"] == "update_status":
            assert "/status" in link["href"]

def test_generate_links_empty_actions():
    """
    Tests that generate_links with an empty actions list returns
    only the 'self' link for the resource.
    """
    links = generate_links("car", 1, [])
    assert isinstance(links, list)
    assert links == [{"rel": "self", "href": "/api/v1/car/1"}]

def test_generate_links_invalid_resource():
    """
    Tests how generate_links handles an invalid or unusual resource name.
    Checks that the link is still generated, even if the URL is odd.
    """
    links = generate_links("???", 99, ["view"])
    assert links[0]["rel"] == "self"
    assert "???" in links[0]["href"]

def test_generate_links_no_id():
    """
    Tests behavior when resource_id is None.
    Ensures the href is still generated and contains 'None' or ends with '/'.
    """
    links = generate_links("car", None, ["view"])
    assert isinstance(links, list)
    assert "None" in links[0]["href"] or links[0]["href"].endswith("/")

def test_generate_links_duplicate_actions():
    """
    Tests how generate_links behaves when duplicate actions are provided.
    In this implementation, duplicates are included, so two 'update' relations are expected.
    """
    links = generate_links("car", 5, ["update", "update", "view"])
    rels = [l['rel'] for l in links]
    # Gali būti du "update"
    assert rels.count("update") == 2
