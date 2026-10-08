import re


ENTITY_TYPES = {
    "PERSON",
    "LOCATION",
    "VEHICLE",
    "PHONE",
    "ORGANIZATION",
    "MONEY"
}

RELATIONSHIP_TYPES = {
    "MET",
    "CONTACTED",
    "TRANSFERRED_MONEY",
    "OWNS",
    "VISITED",
    "WORKS_FOR",
    "CONNECTED_TO"
}


def analyze_text(text):
    """
    Input:
        Raw investigation text

    Output:
        Fixed JSON-compatible structure containing
        entities, relationships and insights.
    """

    entities = []
    relationships = []

    entity_map = {}

    def add_entity(name, entity_type):
        key = (name, entity_type)

        if key not in entity_map:
            prefix = {
                "PERSON": "p",
                "LOCATION": "l",
                "VEHICLE": "v",
                "PHONE": "ph",
                "ORGANIZATION": "o",
                "MONEY": "m"
            }[entity_type]

            entity_id = f"{prefix}{sum(
                1 for e in entities if e["type"] == entity_type
            ) + 1}"

            entity = {
                "id": entity_id,
                "name": name,
                "type": entity_type
            }

            entities.append(entity)
            entity_map[key] = entity_id

        return entity_map[key]

    # -------------------------
    # MONEY
    # -------------------------

    money_pattern = r"(₹[\d,]+|\$\d+(?:,\d+)*)"

    for match in re.findall(money_pattern, text):
        add_entity(match, "MONEY")

    # -------------------------
    # VEHICLE
    # -------------------------

    vehicle_pattern = r"\b[A-Z]{2}\d{2}[A-Z]{1,3}\d{4}\b"

    for match in re.findall(vehicle_pattern, text):
        add_entity(match, "VEHICLE")

    # -------------------------
    # PHONE
    # -------------------------

    phone_pattern = r"\b(?:\+91[- ]?)?[6-9]\d{9}\b"

    for match in re.findall(phone_pattern, text):
        add_entity(match, "PHONE")

    # -------------------------
    # LOCATIONS
    # -------------------------

    location_pattern = r"\b(?:Park Street|Salt Lake|New Town|Kolkata)\b"

    for match in re.findall(location_pattern, text, re.IGNORECASE):
        add_entity(match, "LOCATION")

    # -------------------------
    # ORGANIZATIONS
    # -------------------------

    organization_pattern = r"\b[A-Z][A-Za-z0-9]*(?: Solutions| Technologies| Corporation| Ltd| Inc)\b"

    for match in re.findall(organization_pattern, text):
        add_entity(match.strip(), "ORGANIZATION")

    # -------------------------
    # PERSONS
    # -------------------------

    known_people = [
        "Rahul",
        "Arjun",
        "Vikram",
        "Sameer",
        "Amit",
        "Rohan",
        "Priya"
    ]

    for person in known_people:
        if re.search(rf"\b{re.escape(person)}\b", text):
            add_entity(person, "PERSON")

    # -------------------------
    # RELATIONSHIPS
    # -------------------------

    def get_person(name):
        return entity_map.get((name, "PERSON"))

    def get_entity(name, entity_type):
        return entity_map.get((name, entity_type))

    # Rahul met Arjun
    for a, b in re.findall(
        r"\b(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)\s+met\s+"
        r"(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)\b",
        text,
        re.IGNORECASE
    ):
        source = get_person(a.capitalize())
        target = get_person(b.capitalize())

        if source and target:
            relationships.append({
                "source": source,
                "target": target,
                "type": "MET"
            })

    # contacted
    for a, b in re.findall(
        r"\b(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)\s+contacted\s+"
        r"(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)\b",
        text,
        re.IGNORECASE
    ):
        source = get_person(a.capitalize())
        target = get_person(b.capitalize())

        if source and target:
            relationships.append({
                "source": source,
                "target": target,
                "type": "CONTACTED"
            })

    # transferred money
    for a, amount, b in re.findall(
        r"\b(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)"
        r"\s+transferred\s+(₹[\d,]+|\$\d+(?:,\d+)*)\s+to\s+"
        r"(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)\b",
        text,
        re.IGNORECASE
    ):
        source = get_person(a.capitalize())
        target = get_person(b.capitalize())
        money = get_entity(amount, "MONEY")

        if source and target:
            relationships.append({
                "source": source,
                "target": target,
                "type": "TRANSFERRED_MONEY",
                "amount": money
            })

    # owns vehicle
    for person, vehicle in re.findall(
        r"\b(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)"
        r"\s+owns\s+(?:vehicle\s+)?([A-Z]{2}\d{2}[A-Z]{1,3}\d{4})\b",
        text,
        re.IGNORECASE
    ):
        source = get_person(person.capitalize())
        target = get_entity(vehicle.upper(), "VEHICLE")

        if source and target:
            relationships.append({
                "source": source,
                "target": target,
                "type": "OWNS"
            })

    # works for
    for person, organization in re.findall(
        r"\b(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)"
        r"\s+works\s+for\s+([A-Z][A-Za-z0-9]*(?: Solutions| Technologies| Corporation| Ltd| Inc))",
        text
    ):
        source = get_person(person.capitalize())
        target = get_entity(organization.strip(), "ORGANIZATION")

        if source and target:
            relationships.append({
                "source": source,
                "target": target,
                "type": "WORKS_FOR"
            })

    # visited location
    for person, location in re.findall(
        r"\b(Rahul|Arjun|Vikram|Sameer|Amit|Rohan|Priya)"
        r"\s+(?:visited|met at)\s+"
        r"(Park Street|Salt Lake|New Town|Kolkata)\b",
        text,
        re.IGNORECASE
    ):
        source = get_person(person.capitalize())

        location_name = location.title()

        target = get_entity(location_name, "LOCATION")

        if source and target:
            relationships.append({
                "source": source,
                "target": target,
                "type": "VISITED"
            })

    insights = calculate_insights(entities, relationships)

    return {
        "entities": entities,
        "relationships": relationships,
        "insights": insights
    }


def calculate_insights(entities, relationships):
    connection_count = {}

    for entity in entities:
        connection_count[entity["id"]] = 0

    for relationship in relationships:
        source = relationship["source"]
        target = relationship["target"]

        if source in connection_count:
            connection_count[source] += 1

        if target in connection_count:
            connection_count[target] += 1

    insights = []

    for entity in entities:
        count = connection_count[entity["id"]]

        if entity["type"] == "PERSON" and count >= 3:
            insights.append({
                "entity": entity["name"],
                "reason": "Highly connected node",
                "connections": count
            })

    return insights