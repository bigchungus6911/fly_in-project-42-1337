from __future__ import annotations
import heapq
from typing import Dict, List, Optional, Tuple
from models import Graph


def shortest_path(graph: Graph, start: str, end: str) -> Optional[List[str]]:
    """
    Dijkstra using zone move cost as node-entering cost.
    Path output is list of zone names from start to end.
    """

    dist: Dict[str, float] = {z: float("inf") for z in graph.zones}
    prev: Dict[str, Optional[str]] = {z: None for z in graph.zones}

    # (distance, priority_penalty, zone)
    # priority zone gets slight bonus by using smaller penalty
    pq: List[Tuple[float, int, str]] = []

    dist[start] = 0.0
    heapq.heappush(pq, (0.0, 0, start))

    while pq:
        current_dist, _, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        if u == end:
            break

        for v in graph.adjacency[u]:
            zone_v = graph.zones[v]
            if zone_v.is_blocked():
                continue

            step = zone_v.move_cost()
            nd = current_dist + step

            # tiny tie-break: prefer priority zones
            priority_penalty = 0 if zone_v.zone_type == "priority" else 1

            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, priority_penalty, v))

    if dist[end] == float("inf"):
        return None

    # rebuild
    path: List[str] = []
    cur: Optional[str] = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path
