from collections import defaultdict
from typing import Dict, List, Any

def compute_insights(entities: List[Dict[str, Any]], relationships: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Calculates connection degrees and surfaces central nodes or money movers.
    """
    if not entities or not relationships:
        return []

    id_to_name = {e["id"]: e.get("name", e["id"]) for e in entities}
    id_to_type = {e["id"]: e.get("type", "UNKNOWN") for e in entities}
    
    degree_counts = defaultdict(int)
    money_nodes = set()

    for rel in relationships:
        src = rel.get("source")
        tgt = rel.get("target")
        rel_type = rel.get("type")

        if src in id_to_name:
            degree_counts[src] += 1
        if tgt in id_to_name:
            degree_counts[tgt] += 1

        if rel_type == "TRANSFERRED_MONEY":
            if src in id_to_name and id_to_type.get(src) == "PERSON":
                money_nodes.add(src)
            if tgt in id_to_name and id_to_type.get(tgt) == "PERSON":
                money_nodes.add(tgt)

    insights = []
    
    # Identify high-connectivity nodes
    if degree_counts:
        max_deg = max(degree_counts.values())
        for node_id, count in degree_counts.items():
            if count >= 3 or (count == max_deg and count > 1):
                name = id_to_name.get(node_id, node_id)
                node_type = id_to_type.get(node_id, "ENTITY")
                insights.append({
                    "entity": name,
                    "reason": f"Highly connected {node_type.lower()} with {count} recorded interactions."
                })

    # Flag financial bridge nodes
    for node_id in money_nodes:
        name = id_to_name.get(node_id, node_id)
        if not any(ins["entity"] == name and "financial" in ins["reason"].lower() for ins in insights):
            insights.append({
                "entity": name,
                "reason": "Directly involved in transaction/fund movement."
            })

    return insights