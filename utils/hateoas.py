def generate_links(resource: str, resource_id: int, actions: list[str] = None) -> list[dict]:
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
