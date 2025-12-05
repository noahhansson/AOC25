from utils import read_input, timer, setup_args

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("05", test=test)

    ranges: list[tuple[int, int]] = []
    ingredients: list[int] = []

    for row in inpt:
        if "-" in row:
            lower, upper = row.split("-")
            ranges.append((int(lower), int(upper)))
        elif row != "":
            ingredients.append(int(row))

    return ranges, ingredients

@timer
def get_first_solution(test: bool = False):
    ranges, ingredients = parse_input(test)
    s = sum(any(filter(lambda x: (x[0] <= i) and (x[1] >= i), ranges)) for i in ingredients)
    return s

@timer
def get_second_solution(test: bool = False):
    ranges, _ = parse_input(test)
    ranges = sorted(ranges, key=lambda x: x[0])
    merged_ranges: list[tuple[int, int]] = []
    current_max = 0

    for start, end in ranges:
        if not merged_ranges:
            merged_ranges.append((start, end))
            current_max = end
            continue

        new_start = max([current_max + 1, start])
        if new_start > end:
            continue
        else:
            merged_ranges.append((new_start, end))
            current_max = end

    return sum([r[1] - r[0] + 1 for r in merged_ranges])

print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
