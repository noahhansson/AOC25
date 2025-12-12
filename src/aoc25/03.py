from utils import read_input, timer, setup_args

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("03", test=test)
    return [tuple(int(x) for x in bank) for bank in inpt]


def solve(bank: tuple[int, ...], num_to_enable: int) -> int:
    if num_to_enable == 0:
        return 0
    max_idx = -1
    max_digit = -1
    for i, battery in enumerate(bank):
        if battery > max_digit:
            max_idx = i
            max_digit = battery
        if (battery == 9) or ((i + num_to_enable) >= len(bank)):
            break

    return int(
        (10 ** (num_to_enable - 1)) * bank[max_idx]
        + solve(bank[max_idx + 1 :], num_to_enable - 1)
    )


@timer
def get_first_solution(test: bool = False):
    banks = parse_input(test)

    joltage_sum = 0

    for bank in banks:
        joltage = solve(bank, 2)
        joltage_sum += joltage
    return joltage_sum


@timer
def get_second_solution(test: bool = False):
    banks = parse_input(test)
    joltage_sum = 0
    for bank in banks:
        joltage = solve(bank, 12)
        joltage_sum += joltage
    return joltage_sum


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
