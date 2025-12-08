from utils import read_input, timer, setup_args
from dataclasses import dataclass
from typing import Self
from functools import reduce
from collections import deque, defaultdict

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

def calc_distances(junctions: list[Point3]) -> list[tuple[Point3, Point3, int]]:
    distances: list[tuple[Point3, Point3, int]] = []
    for j1 in junctions:
        for j2 in junctions:
            if j1 == j2:
                continue
            else:
                distances.append((j1, j2, j1.dist(j2)))

    return sorted(distances, key=lambda x: x[2])

@timer
def get_first_solution(test: bool = False):
    junctions = parse_input(test)

    connections: dict[Point3, set[Point3]] = defaultdict(set)
    distances = calc_distances(junctions)

    n_iter = 10 if test else 1000
    for _ in range(n_iter):

        j1 = j2 = None
        for j1, j2, _ in distances:
            if j2 not in connections[j1]:
                break

        assert j1 is not None
        assert j2 is not None
        if j2 in connections[j1]:
            continue
        else:
            connections[j1] |= {j2}
            connections[j2] |= {j1}

    circuits = set()
    seen = set()
    for j in junctions:
        if j in seen:
            continue
        circuit = set()
        queue = deque([j])
        while queue:
            c = queue.popleft()
            if c in seen:
                continue
            seen.add(c)
            circuit.add(c)
            for adj in connections[c]:
                if adj not in seen:
                    queue.append(adj)
        circuits.add(frozenset(circuit))

    return reduce(lambda x, y: x*len(y), sorted(circuits, key=lambda c: len(c), reverse=True)[:3], initial=1)

@timer
def get_second_solution(test: bool = False):
    junctions = parse_input(test)

    connections: dict[Point3, set[Point3]] = defaultdict(set)
    distances = calc_distances(junctions)

    i = 0
    while True:

        j1 = j2 = None
        for j1, j2, _ in distances:
            c1 = connections[j1]
            c2 = connections[j2]
            if c1 is not c2:
                break

        assert j1 is not None
        assert j2 is not None
        circuit = connections[j1] | connections[j2] | {j1, j2}
        for j in circuit:
            connections[j] = circuit

        if len(junctions) == len(circuit):
            return j1.x * j2.x

        i += 1

print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
