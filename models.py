from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Tuple


# small helper: accepted zone types and default move costs
ZONE_MOVE_COST = {
    "normal": 1,
    "priority": 1,     # same cost but can be preferred in pathfinding tie-break
    "restricted": 2,   # takes 2 turns to enter
    "blocked": 999999  # basically impossible
}


@dataclass
class Zone:
    name: str
    role: str  # start_hub, end_hub, hub
    zone_type: str = "normal"
    max_drones: int = 1
    color: Optional[str] = None

    def move_cost(self) -> int:
        return ZONE_MOVE_COST.get(self.zone_type, 1)

    def is_blocked(self) -> bool:
        return self.zone_type == "blocked"


@dataclass
class Connection:
    a: str
    b: str
    max_link_capacity: int = 1

    def key(self) -> Tuple[str, str]:
        # normalize direction for capacity tracking
        return tuple(sorted((self.a, self.b)))


@dataclass
class Drone:
    drone_id: int
    current_zone: str
    finished: bool = False
    # if drone is currently moving to a restricted zone, we keep "time left"
    traveling_to: Optional[str] = None
    travel_time_left: int = 0


@dataclass
class Graph:
    zones: Dict[str, Zone] = field(default_factory=dict)
    adjacency: Dict[str, Set[str]] = field(default_factory=dict)
    connections: Dict[Tuple[str, str], Connection] = field(default_factory=dict)
    start_zone: Optional[str] = None
    end_zone: Optional[str] = None

    def add_zone(self, zone: Zone) -> None:
        if zone.name in self.zones:
            raise ValueError(f"Duplicate zone name: {zone.name}")
        self.zones[zone.name] = zone
        self.adjacency.setdefault(zone.name, set())

        if zone.role == "start_hub":
            if self.start_zone is not None:
                raise ValueError("Multiple start_hub definitions")
            self.start_zone = zone.name
        elif zone.role == "end_hub":
            if self.end_zone is not None:
                raise ValueError("Multiple end_hub definitions")
            self.end_zone = zone.name

    def add_connection(self, conn: Connection) -> None:
        if conn.a not in self.zones or conn.b not in self.zones:
            raise ValueError(f"Invalid connection: {conn.a}-{conn.b} (zone missing)")
        key = conn.key()
        if key in self.connections:
            raise ValueError(f"Duplicate connection: {conn.a}-{conn.b}")
        self.connections[key] = conn
        self.adjacency[conn.a].add(conn.b)
        self.adjacency[conn.b].add(conn.a)

    def get_connection(self, z1: str, z2: str) -> Connection:
        key = tuple(sorted((z1, z2)))
        return self.connections[key]
