"""
app/utils/hateoas.py

Utility for generating HATEOAS links for API resources.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Provides a helper function to generate HATEOAS (Hypermedia as the Engine of Application State)
    links for any API resource, supporting "self", "update", "delete" and "update_status" relations.
    Used in API responses to provide navigable links for the frontend.

Usage:
    Call generate_links(resource, resource_id, actions) in endpoint response construction.
"""

def generate_links(resource: str, resource_id: int, actions: list[str] = None) -> list[dict]:
    """
    Generates HATEOAS links for a given API resource.

    Args:
        resource (str): The resource name (e.g., 'invoice', 'reservation').
        resource_id (int): The unique identifier of the resource.
        actions (list[str], optional): List of actions for which to generate links.
            Supported actions: "update", "delete", "update_status".

    Returns:
        list[dict]: A list of dictionaries representing HATEOAS links.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
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
