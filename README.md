# Fly-in

## Description
This project simulates drones moving from a `start_hub` to an `end_hub` on a custom graph.
It handles zone capacity, connection capacity, movement costs, and basic pathfinding.

## Instructions
### Run
```bash
python3 main.py path/to/map.txt
```

### Run with capacity info
```bash
python3 main.py --capacity-info path/to/map.txt
```

## Algorithm explanation
- The parser reads the map file and builds a custom graph (`Zone` + `Connection`).
- Pathfinding uses Dijkstra shortest path with zone movement cost:
  - normal: 1
  - priority: 1 (preferred on tie)
  - restricted: 2
  - blocked: not allowed
- The simulation is turn-based:
  - each drone tries to move to the next zone in path
  - movement is allowed only if zone and connection capacities are available
  - restricted zones take 2 turns to enter
- Output prints movements by turn and hides stationary drones.

## Visual representation
Current version uses terminal output.
The `--capacity-info` flag gives extra visual context:
- zone usage (`used/max`)
- connection usage (`used/max`)

This helps understand congestion and bottlenecks while simulation runs.

## Example input
```txt
nb_drones: 3
start_hub: A zone=normal max_drones=10
hub: B zone=normal max_drones=1
hub: C zone=restricted max_drones=1
end_hub: D zone=priority max_drones=10
connection: A-B max_link_capacity=1
connection: B-C max_link_capacity=1
connection: C-D max_link_capacity=1
```

## Expected output (example style)
```txt
D1-B
D1-B-C D2-B
D1-C D2-B-C D3-B
D1-D D2-C D3-B-C
...
```
Actual turn lines can vary based on map and capacities.
