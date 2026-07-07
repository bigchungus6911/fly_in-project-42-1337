from dataclasses import dataclass, field
from typing import Optional
from models.zone import Zone
from models.connection import Connection

@dataclass
class Graph:
    zones: dict[str, Zone] = field(default_factory=dict)#zone name and its object in a dict
    adjacency: dict[str, list[Connection]] = field(default_factory=dict)
    
    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone #creat a zone
        self.adjacency[zone.name] = [] # creat emtpy connection list for the zone

    def add_connection(self, conn: Connection) -> None:
        self.adjacency[conn.zone1_name].append(conn)#add connection to zone1 
        self.adjacency[conn.zone2_name].append(conn)#add connection to zone2

    def get_neighors(self, zone_name: str ) -> list[Zone]:
        neighbors = []
        for conn in self.adjacency[zone_name]:
            if conn.zone1_name == zone_name:
                neighbors.append(self.zones[conn.zone2_name])
            else:
                neighbors.append(self.zones[conn.zone1_name])
        return neighbors
    