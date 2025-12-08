from utils import read_input, timer, setup_args
from dataclasses import dataclass
from typing import Self
from functools import reduce
from typing import Iterable

args = setup_args()

@dataclass(frozen=True, repr=False)
class Point3:
    x: int
    y: int
    z: int

    def dist(self, other: Self) -> float:
        #Skip sqrt since it's monotonic
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    def __lt__(self, other: Self) -> bool:
        return self.x < other.x


def parse_input(test: bool = False) -> list[Point3]:
    inpt = read_input("08", test=test)
    junctions: list[Point3] = []
    for row in inpt:
        junctions.append(Point3(*[int(x) for x in row.split(",")]))
    return junctions

@timer
def get_first_solution(test: bool = False):
    junctions = parse_input(test)

    connections: dict[Point3, set[Point3]] = {}

    n_iter = 10 if test else 1000
    for _ in range(n_iter):
        print(_)
        shortest = 1e999
        shortest_j1 = None
        shortest_j2 = None

        for i, j1 in enumerate(junctions):
            for j2 in junctions[i + 1:]:
                if (j1 < j2 and j2 in connections.get(j1, set())) or (j2 < j1 and j1 in connections.get(j2, set())):
                    continue

                if ((d := j1.dist(j2)) < shortest):
                    shortest = d
                    shortest_j1 = j1
                    shortest_j2 = j2

        if shortest_j1 is not None and shortest_j2 is not None:
            j1_circuit = connections.get(shortest_j1, set())
            j2_circuit = connections.get(shortest_j2, set())

            j1_circuit |= j2_circuit.union({shortest_j2})
            j2_circuit |= j1_circuit.union({shortest_j1})

            connections[shortest_j1] = j1_circuit
            connections[shortest_j2] = j2_circuit
            
        else:
            raise RuntimeError()

    all_circuits = set([frozenset(s) for s in connections.values()])
    print(all_circuits)
    return reduce(lambda x, y: x*len(y), sorted(all_circuits, key=lambda c: len(c), reverse=True)[:3], initial=1)


@timer
def get_second_solution(test: bool = False):
    inpt = parse_input(test)

    return inpt


print(f"P1: {get_first_solution(test=args.test)}")
# print(f"P2: {get_second_solution(test=args.test)}")
