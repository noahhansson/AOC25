from utils import read_input, timer, setup_args

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("05", test=test)

    ranges: set[tuple[int, int]] = set()
    ingredients: set[int] = set()

    for row in inpt:
        if "-" in row:
            lower, upper = row.split("-")
            ranges.add((int(lower), int(upper)))
        elif row != "":
            ingredients.add(int(row))

    return ranges, ingredients

def is_in_range(ingredient, ranges) -> bool:
    valid_lower = filter(lambda x: x[0] <= ingredient, ranges)
    valid_upper = filter(lambda x: x[1] >= ingredient, valid_lower)

    return len(list(valid_upper)) > 0

@timer
def get_first_solution(test: bool = False):
    ranges, ingredients = parse_input(test)
    s = sum(is_in_range(i, ranges) for i in ingredients)

    return s

@timer
def get_second_solution(test: bool = False):
    ranges, _ = parse_input(test)

    s = 0
    overlap = 0
    for r in ranges:
        other_ranges = ranges - {r}
        s += r[1] - r[0] + 1

        left_overlap = list(filter(lambda x: (x[0] <= r[0]) and (x[1] >= r[0]), other_ranges))
        if left_overlap:
            left_overlap_len = max([o[1] for o in left_overlap]) - r[0] + 1
            overlap += left_overlap_len

        right_overlap = list(filter(lambda x: (x[0] <= r[1]) and (x[1] >= r[1]), other_ranges))
        if right_overlap:
            right_overlap_len = r[1] - min([o[0] for o in right_overlap]) + 1
            overlap += right_overlap_len

    return s - overlap // 2

print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
