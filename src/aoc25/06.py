from utils import read_input, timer, setup_args
from functools import reduce

args = setup_args()


def parse_input(test: bool = False) -> tuple[list[list[list[str]]], list[str]]:
    inpt = read_input("06", test=test)
    cols: list[list[list[str]]] = []
    ops: list[str] = []

    n_rows = len(inpt)
    buffer: list[list[str]] = [[] for j in range(n_rows - 1)]
    op = "+"
    for i in range(len(inpt[-1])):
        if (inpt[-1][i] == "+") or (inpt[-1][i] == "*"):
            if any(buffer):
                cols.append(buffer)
                ops.append(op)
            buffer = [[] for j in range(n_rows - 1)]
            op = inpt[-1][i]

        for j in range(n_rows - 1):
            buffer[j].append(inpt[j][i].replace("\n", " "))
    else:
        cols.append(buffer)
        ops.append(op)
            
    return cols, ops


@timer
def get_first_solution(test: bool = False):
    cols, ops = parse_input(test)
    total = 0
    for i in range(len(cols)):
        op = ops[i]
        terms = [int("".join(x).replace(" ", "")) for x in cols[i]]
        if op == "*":
            total += reduce(lambda x, y: x * y, terms, initial=1)
        elif op == "+":
            total += reduce(lambda x, y: x + y, terms, initial=0)

    return total


@timer
def get_second_solution(test: bool = False):
    cols, ops = parse_input(test)
    total = 0
    for i in range(len(cols)):
        op = ops[i]
        cols_t = list(map(list, zip(*cols[i])))
        terms = [int("".join(x).replace(" ", "")) for x in cols_t if not all([c==" " for c in x])]
        if op == "*":
            total += reduce(lambda x, y: x * y, terms, initial=1)
        elif op == "+":
            total += reduce(lambda x, y: x + y, terms, initial=0)

    return total


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
