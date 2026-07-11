from __future__ import annotations
import argparse
import sys

from parser import parse_file
from simulator import run_simulation


def main() -> int:
    parser = argparse.ArgumentParser(description="Fly-in drone simulation")
    parser.add_argument("map_file", help="Path to map file")
    parser.add_argument("--capacity-info", action="store_true", help="Show capacity usage each turn")
    args = parser.parse_args()

    try:
        graph, nb_drones = parse_file(args.map_file)
        lines = run_simulation(graph, nb_drones, show_capacity=args.capacity_info)
        for line in lines:
            print(line)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
