from utils import read_input, timer, setup_args
from itertools import combinations

args = setup_args()


def parse_input(test: bool = False) -> list[tuple[int, int]]:
    inpt = read_input("09", test=test)
    tiles: list[tuple[int, int]] = []
    for row in inpt:
        tiles.append(tuple(int(x) for x in row.split(",")))
    return tiles


@timer
def get_first_solution(test: bool = False):
    tiles = parse_input(test)
    max_area = 0
    for t1, t2 in combinations(tiles, 2):
        area = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
        if area > max_area:
            max_area = area

    return max_area


@timer
def get_second_solution(test: bool = False):
    tiles = parse_input(test)
    max_area = 0

    vlines = []
    hlines = []

    for (x1, y1), (x2, y2) in zip(tiles, tiles[1:] + tiles[:1]):
        if x1==x2:
            vlines.append((x1, (min(y1, y2), max(y1, y2))))
        elif y1==y2:
            hlines.append(((min(x1, x2), max(x1, x2)), y1))

    for t1, t2 in combinations(tiles, 2):

        area = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
        if area <= max_area:
            continue

        valid = True

        xmin, xmax = sorted((t1[0], t2[0]))
        ymin, ymax = sorted((t1[1], t2[1]))

        # Check vertices inside of rectangle
        for x, y in tiles:
            if (xmin < x < xmax) and (ymin < y < ymax):
                valid = False
                break

        # Ray-cast ((xmin, xmax), ymid) and (xmid, (ymin, ymax)) 
        # and check intersections with edges
        xmid = xmin + (xmax - xmin) // 2
        ymid = ymin + (ymax - ymin) // 2

        for x, (y1, y2) in vlines:
            if (y1 < ymid < y2) and (xmin < x < xmax):
                valid = False
                break
        for (x1, x2), y in hlines:
            if (x1 < xmid < x2) and (ymin < y < ymax):
                valid = False
                break
            
        if not valid:
            continue

        max_area = area

    return max_area


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
