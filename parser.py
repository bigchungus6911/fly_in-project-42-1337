from __future__ import annotations
from typing import Dict
from models import Graph, Zone, Connection


def _parse_kv_items(part: str) -> Dict[str, str]:
    """
    parse "x=1 y=2" into {"x": "1", "y": "2"}
    very simple split; good enough for this project format
    """
    out: Dict[str, str] = {}
    tokens = part.strip().split()
    for t in tokens:
        if "=" not in t:
            continue
        k, v = t.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def parse_file(path: str) -> tuple[Graph, int]:
    graph = Graph()
    nb_drones = None

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line_no, raw in enumerate(lines, start=1):
        line = raw.strip()

        # ignore comments and empty lines
        if not line or line.startswith("#"):
            continue

        # nb_drones
        if line.startswith("nb_drones:"):
            if nb_drones is not None:
                raise ValueError(f"Line {line_no}: duplicate nb_drones")
            right = line.split(":", 1)[1].strip()
            if not right.isdigit() or int(right) <= 0:
                raise ValueError(f"Line {line_no}: invalid nb_drones value")
            nb_drones = int(right)
            continue

        # zone lines: start_hub:, end_hub:, hub:
        if line.startswith("start_hub:") or line.startswith("end_hub:") or line.startswith("hub:"):
            role, rest = line.split(":", 1)
            rest = rest.strip()
            if not rest:
                raise ValueError(f"Line {line_no}: empty zone definition")

            # first token is zone name, remaining are metadata
            parts = rest.split(maxsplit=1)
            zone_name = parts[0]
            meta_text = parts[1] if len(parts) > 1 else ""
            meta = _parse_kv_items(meta_text)

            zone_type = meta.get("zone", "normal")
            if zone_type not in {"normal", "restricted", "priority", "blocked"}:
                raise ValueError(f"Line {line_no}: invalid zone type '{zone_type}'")

            max_drones_str = meta.get("max_drones", "1")
            if not max_drones_str.isdigit() or int(max_drones_str) <= 0:
                raise ValueError(f"Line {line_no}: invalid max_drones")
            max_drones = int(max_drones_str)

            color = meta.get("color")

            zone = Zone(
                name=zone_name,
                role=role,
                zone_type=zone_type,
                max_drones=max_drones,
                color=color
            )
            graph.add_zone(zone)
            continue

        # connection lines
        if line.startswith("connection:"):
            rest = line.split(":", 1)[1].strip()
            if not rest:
                raise ValueError(f"Line {line_no}: empty connection definition")

            parts = rest.split(maxsplit=1)
            edge = parts[0]
            meta_text = parts[1] if len(parts) > 1 else ""
            meta = _parse_kv_items(meta_text)

            if "-" not in edge:
                raise ValueError(f"Line {line_no}: invalid connection format")
            a, b = edge.split("-", 1)
            a = a.strip()
            b = b.strip()
            if not a or not b:
                raise ValueError(f"Line {line_no}: invalid connection nodes")

            cap_str = meta.get("max_link_capacity", "1")
            if not cap_str.isdigit() or int(cap_str) <= 0:
                raise ValueError(f"Line {line_no}: invalid max_link_capacity")
            cap = int(cap_str)

            graph.add_connection(Connection(a=a, b=b, max_link_capacity=cap))
            continue

        raise ValueError(f"Line {line_no}: unknown line format")

    # final checks
    if nb_drones is None:
        raise ValueError("Missing nb_drones")
    if graph.start_zone is None:
        raise ValueError("Missing start_hub")
    if graph.end_zone is None:
        raise ValueError("Missing end_hub")

    return graph, nb_drones
