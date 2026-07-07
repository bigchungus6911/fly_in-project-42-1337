from dataclasses import dataclass, field

@dataclass
class Connection:#connection between two zones got zones names and some other data hh
    zone1_name: str
    zone2_name: str
    max_link_capacity: int = 1
    current_usage: int = field(default=0, repr=False)
