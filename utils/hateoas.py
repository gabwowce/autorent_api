"""
utils/hateoas.py

Utility function for generating HATEOAS links for REST API responses.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Builds standardized HATEOAS-style navigation links for a given resource.
    Supports actions such as update, delete, and update_status.
"""

def generate_links(resource: str, resource_id: int, actions: list[str] = None) -> list[dict]:
    """
    Generate HATEOAS links for a resource.

    Args:
        resource (str): Resource name (e.g., "cars").
        resource_id (int): Unique ID of the resource.
        actions (list[str], optional): Additional actions (e.g., "update", "delete", "update_status").

    Returns:
        list[dict]: List of dictionaries representing navigation links.

    Example:
        generate_links("cars", 5, ["update", "delete"]) → [
            {"rel": "self", "href": "/api/v1/cars/5"},
            {"rel": "update", "href": "/api/v1/cars/5"},
            {"rel": "delete", "href": "/api/v1/cars/5"}
        ]
    """
    base_url = f"/api/v1/{resource}/{resource_id}"
    links = [{"rel": "self", "href": base_url}]
    if actions:
        for action in actions:
            if action == "update":
                links.append({"rel": "update", "href": base_url})
            elif action == "delete":
                links.append({"rel": "delete", "href": base_url})
            elif action == "update_status":
                links.append({"rel": "update_status", "href": f"{base_url}/status"})
    return links
