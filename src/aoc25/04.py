from utils import read_input, timer, setup_args
from itertools import product

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("04", test=test)
    
    rolls: set[tuple[int, int]] = set()

    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "@":
                rolls.add((x, y))

    return rolls

def get_adj(p: tuple[int, int]) -> set[tuple[int, int]]:
    adj: set[tuple[int, int]] = set()
    for c in product((-1, 0, 1), (-1, 0, 1)):
        if c != (0, 0):
            adj.add((p[0] + c[0], p[1] + c[1]))

    return adj


@timer
def get_first_solution(test: bool = False):
    rolls = parse_input(test)

    n_accessed = 0
    for roll in rolls:
        n_adj = sum([adj in rolls for adj in get_adj(roll)])
        if n_adj < 4:
            n_accessed += 1

    return n_accessed


@timer
def get_second_solution(test: bool = False):
    rolls = parse_input(test)
    removed: set[tuple[int, int]] = set()
    to_remove: set[tuple[int, int]] = set()

    while True:
        to_remove = set()
        for roll in rolls:
            n_adj = sum([adj in rolls for adj in get_adj(roll)])
            if n_adj < 4:
                to_remove.add(roll)
                removed.add(roll)
        rolls = rolls - to_remove

        if not to_remove:
            break

    return len(removed)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
