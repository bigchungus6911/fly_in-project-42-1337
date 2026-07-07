from models.zone import Zone, ZoneType
from models.connection import Connection

z1 = Zone(name="hub", x=0, y=0)
z2 = Zone(name="roof1", x=3, y=4, zone_type=ZoneType.RESTRICTED, color="red")
z3 = Zone(name="goal", x=10, y=10, color="yellow")

c1 = Connection(zone1_name="hub", zone2_name="roof1")
c2 = Connection(zone1_name="roof1", zone2_name="goal", max_link_capacity=2)

print(z1)
print(z2)
print(z3)
print(c1)
print(c2)