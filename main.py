from models.zone import Zone, ZoneType
from models.connection import Connection
from models.graph import Graph

z1 = Zone(name="hub", x=0, y=0)
z2 = Zone(name="roof1", x=3, y=4, zone_type=ZoneType.RESTRICTED, color="red")
z3 = Zone(name="goal", x=10, y=10, color="yellow")

c1 = Connection(zone1_name="hub", zone2_name="roof1")
c2 = Connection(zone1_name="roof1", zone2_name="goal", max_link_capacity=2)

g = Graph()
g.add_zone(z1)
g.add_zone(z2)
g.add_zone(z3)
g.add_connection(c1)
g.add_connection(c2)

print(g.get_neighbors("hub"))
print(g.get_neighbors("roof1"))
print(g.get_connection("hub", "roof1"))