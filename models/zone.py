from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class ZoneType(Enum):#class with fixed set of named constants to do like this zonetype.normal 
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: Optional[str] = None
    max_drones: int = 1
    current_drones: int = field(default=0, repr=False)