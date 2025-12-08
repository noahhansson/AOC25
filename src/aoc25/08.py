from utils import read_input, timer, setup_args
from dataclasses import dataclass
from typing import Self
from functools import reduce
from collections import defaultdict
from itertools import combinations

args = setup_args()

@dataclass(frozen=True, repr=False)
class Point3:
    x: int
    y: int
    z: int

    def dist(self, other: Self) -> int:
        #Skip sqrt since it's monotonic
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

def parse_input(test: bool = False) -> list[Point3]:
    inpt = read_input("08", test=test)
    junctions: list[Point3] = []
    for row in inpt:
        junctions.append(Point3(*[int(x) for x in row.split(",")]))
    return junctions

def calc_distances(junctions: list[Point3]) -> list[tuple[Point3, Point3]]:
    return sorted([(j1, j2) for j1, j2 in combinations(junctions, 2)], key=lambda x: x[0].dist(x[1]))

@timer
def get_first_solution(test: bool = False):
    junctions = parse_input(test)
    distances = calc_distances(junctions)
    circuits: dict[Point3, set[Point3]] = defaultdict(set)

    n_iter = 10 if test else 1000
    for i, (j1, j2) in enumerate(distances):
        if i == n_iter:
            break
        c1 = circuits[j1]
        c2 = circuits[j2]
        if c1 is c2:
            continue

        circuit = circuits[j1] | circuits[j2] | {j1, j2}
        for j in circuit:
            circuits[j] = circuit

    unique_circuits = set(frozenset(c) for c in circuits.values())
    return reduce(lambda x, y: x*len(y), sorted(unique_circuits, key=lambda c: len(c), reverse=True)[:3], initial=1)

@timer
def get_second_solution(test: bool = False):
    junctions = parse_input(test)
    distances = calc_distances(junctions)
    circuits: dict[Point3, set[Point3]] = defaultdict(set)

    for j1, j2 in distances:
        c1 = circuits[j1]
        c2 = circuits[j2]
        if c1 is c2:
            continue

        circuit = circuits[j1] | circuits[j2] | {j1, j2}
        for j in circuit:
            circuits[j] = circuit

        if len(junctions) == len(circuit):
            return j1.x * j2.x

print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
