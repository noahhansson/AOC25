from utils import read_input, timer, setup_args

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("01", test=test)
    return inpt


@timer
def get_first_solution(test: bool = False):
    inpt = parse_input(test)

    score = 0
    pointer = 50

    for row in inpt:
        r = row[0]
        dist = int(row[1:])
        if r == "L":
            dist = -dist

        pointer += dist
        pointer = pointer % 100

        if pointer == 0:
            score += 1

    return score


@timer
def get_second_solution(test: bool = False):
    inpt = parse_input(test)

    score = 0
    pointer = 50

    for row in inpt:
        r = row[0]
        dist = int(row[1:])

        prev = pointer
        if r == "L":
            pointer -= dist
        else:
            pointer += dist

        clicks = abs(pointer // 100)
        if pointer == 0:
            clicks += 1
        if (r == "L") and (dist > 100) and (pointer % 100 == 0):
            clicks += 1
        if (prev == 0) and (r == "L"):
            clicks -= 1

        score += clicks
        pointer = pointer % 100

    return score


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
