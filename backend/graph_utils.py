def get_connection_counts(entities, relationships):
    counts = {
        entity["id"]: 0
        for entity in entities
    }

    for relationship in relationships:
        source = relationship["source"]
        target = relationship["target"]

        if source in counts:
            counts[source] += 1

        if target in counts:
            counts[target] += 1

    result = []

    for entity in entities:
        result.append({
            "id": entity["id"],
            "name": entity["name"],
            "type": entity["type"],
            "connections": counts[entity["id"]]
        })

    return sorted(
        result,
        key=lambda x: x["connections"],
        reverse=True
    )