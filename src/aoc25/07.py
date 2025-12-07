from utils import read_input, timer, setup_args
from collections import defaultdict

args = setup_args()


def parse_input(test: bool = False) -> tuple[tuple[int, int], set[tuple[int, int]]]:
    inpt = read_input("07", test=test)
    start: tuple[int, int] = (-1, -1)
    splitters: set[tuple[int, int]] = set()
    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "S":
                start = (x, y)
            elif c == "^":
                splitters.add((x, y))
    return start, splitters


@timer
def get_first_solution(test: bool = False):
    start, splitters = parse_input(test)
    current_beams: set[int] = set()
    current_beams.add(start[0])
    n_splits = 0
    for y in range(1, max([s[1] for s in splitters]) + 1):
        next_beams = set()
        for beam_x in current_beams:
            if (beam_x, y) in splitters:
                n_splits += 1
                next_beams.add(beam_x + 1)
                next_beams.add(beam_x - 1)
            else:
                next_beams.add(beam_x)
        current_beams = next_beams

    return n_splits


@timer
def get_second_solution(test: bool = False):
    start, splitters = parse_input(test)
    current_beams: dict[int, int] = defaultdict(int)
    current_beams[start[0]] += 1
    for y in range(1, max([s[1] for s in splitters]) + 1):
        next_beams: dict[int, int] = defaultdict(int)
        for beam_x, n in current_beams.items():
            if (beam_x, y) in splitters:
                next_beams[beam_x + 1] += n
                next_beams[beam_x - 1] += n
            else:
                next_beams[beam_x] += n
        current_beams = next_beams

    return sum(current_beams.values())


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
