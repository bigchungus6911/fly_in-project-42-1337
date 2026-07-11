from __future__ import annotations
from typing import Dict, List
from collections import defaultdict
from models import Graph, Drone
from pathfinder import shortest_path


def run_simulation(graph: Graph, nb_drones: int, show_capacity: bool = False) -> List[str]:
    start = graph.start_zone
    end = graph.end_zone
    assert start is not None and end is not None

    # pre-compute one path per drone (simple approach)
    base_path = shortest_path(graph, start, end)
    if base_path is None:
        raise ValueError("No valid path from start_hub to end_hub")

    drones: List[Drone] = [Drone(drone_id=i + 1, current_zone=start) for i in range(nb_drones)]

    # index in path (for each drone)
    path_index: Dict[int, int] = {d.drone_id: 0 for d in drones}

    output_lines: List[str] = []

    while True:
        if all(d.finished for d in drones):
            break

        # occupancy count at start of turn
        zone_occupancy = defaultdict(int)
        for d in drones:
            if not d.finished and d.traveling_to is None:
                zone_occupancy[d.current_zone] += 1

        link_usage = defaultdict(int)
        moved_tokens: List[str] = []

        # process drones in id order (simple deterministic)
        for d in drones:
            if d.finished:
                continue

            # if currently in multi-turn travel (restricted zone entry), continue
            if d.traveling_to is not None:
                d.travel_time_left -= 1
                if d.travel_time_left <= 0:
                    d.current_zone = d.traveling_to
                    d.traveling_to = None
                    if d.current_zone == end:
                        d.finished = True
                    else:
                        moved_tokens.append(f"D{d.drone_id}-{d.current_zone}")
                continue

            # if already at end
            if d.current_zone == end:
                d.finished = True
                continue

            idx = path_index[d.drone_id]
            if idx + 1 >= len(base_path):
                # should not happen but keep safe
                d.finished = True
                continue

            nxt = base_path[idx + 1]
            conn = graph.get_connection(d.current_zone, nxt)
            conn_key = conn.key()

            # check connection capacity
            if link_usage[conn_key] >= conn.max_link_capacity:
                continue

            # check zone capacity (start and end can host many as requested)
            nxt_zone = graph.zones[nxt]
            if nxt not in {start, end}:
                if zone_occupancy[nxt] >= nxt_zone.max_drones:
                    continue

            # move is allowed
            link_usage[conn_key] += 1
            zone_occupancy[d.current_zone] -= 1

            # entering restricted zone takes extra turns
            if nxt_zone.zone_type == "restricted":
                d.traveling_to = nxt
                d.travel_time_left = 2  # takes 2 turns to complete
                path_index[d.drone_id] += 1
                moved_tokens.append(f"D{d.drone_id}-{d.current_zone}-{nxt}")
            else:
                d.current_zone = nxt
                path_index[d.drone_id] += 1
                zone_occupancy[nxt] += 1
                moved_tokens.append(f"D{d.drone_id}-{nxt}")

                if d.current_zone == end:
                    d.finished = True

        # output only if at least one drone moved this turn
        if moved_tokens:
            line = " ".join(moved_tokens)

            if show_capacity:
                # simple readable extra info
                zone_parts = []
                for z_name, z in graph.zones.items():
                    used = zone_occupancy[z_name]
                    # start/end can be overcrowded in logic, still show max for visibility
                    zone_parts.append(f"{z_name}:{used}/{z.max_drones}")

                conn_parts = []
                for key, c in graph.connections.items():
                    used = link_usage[key]
                    conn_parts.append(f"{c.a}-{c.b}:{used}/{c.max_link_capacity}")

                cap_line = " | ZONES " + ", ".join(zone_parts) + " | LINKS " + ", ".join(conn_parts)
                line += cap_line

            output_lines.append(line)

    return output_lines
