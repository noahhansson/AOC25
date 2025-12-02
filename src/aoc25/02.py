from utils import read_input, timer, setup_args
import re

args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("02", test=test)
    inpt_parsed = []
    for r1 in inpt[0].split(","):
        inpt_parsed.append(r1.split("-"))
    
    return inpt_parsed

def detect_dup_id_p1(p_id: str) -> bool:
    pattern = p_id[:len(p_id) // 2]
    next_digits = p_id[len(p_id) // 2:]
    if pattern == next_digits:
        return True
    return False


@timer
def get_first_solution(test: bool = False):
    inpt = parse_input(test)

    invalid_ids = []

    for id_range in inpt:
        lo = int(id_range[0])
        hi = int(id_range[1])

        for p_id in range(lo, hi + 1):
            if detect_dup_id_p1(str(p_id)):
                invalid_ids.append(p_id)

    s = 0
    for p_id in invalid_ids:
        s += p_id

    return s


@timer
def get_second_solution(test: bool = False):
    inpt = parse_input(test)

    return 0


print(f"P1: {get_first_solution(test=args.test)}")
# print(f"P2: {get_second_solution(test=args.test)}")
