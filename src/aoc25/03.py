from utils import read_input, timer, setup_args

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("03", test=test)
    return [[int(x) for x in bank] for bank in inpt]


@timer
def get_first_solution(test: bool = False):
    banks = parse_input(test)

    joltage_sum = 0

    for bank in banks:
        idx_first = -1
        idx_second = -1

        max_digit = -1
        for i, battery in enumerate(bank[:-1]):
            if battery > max_digit:
                idx_first = i
                max_digit = battery
            if battery == 9:
                break
        
        max_digit = -1
        for i, battery in enumerate(bank[idx_first+1:], start=idx_first+1):
            if battery > max_digit:
                idx_second = i
                max_digit = battery
            if battery == 9:
                break

        joltage = 10 * bank[idx_first] + bank[idx_second]

        joltage_sum+= joltage

    return joltage_sum


@timer
def get_second_solution(test: bool = False):
    inpt = parse_input(test)

    return 0


print(f"P1: {get_first_solution(test=args.test)}")
# print(f"P2: {get_second_solution(test=args.test)}")
