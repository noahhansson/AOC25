from utils import read_input, timer, setup_args
from collections import deque
from dataclasses import dataclass

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


@dataclass
class Machine:
    indicator: tuple[int, ...]
    buttons: list[tuple[int, ...]]
    joltage: tuple[int, ...]


args = setup_args()


def parse_input(test: bool = False):
    inpt = read_input("10", test=test)
    machines: list[Machine] = []
    for row in inpt:
        buttons: list[tuple[int, ...]] = []
        indicator: tuple[int, ...] = ()
        joltage: tuple[int, ...] = ()
        for x in row.split(" "):
            if x.startswith("["):
                indicator = tuple(1 if c == "#" else 0 for c in x.strip("[]"))
            if x.startswith("("):
                button_raw = tuple(int(c) for c in x.strip("()").split(","))
                button = tuple(
                    [
                        1 if j in button_raw else 0
                        for j, _ in enumerate(range(len(indicator)))
                    ]
                )
                buttons.append(button)
            if x.startswith("{"):
                joltage = tuple(int(c) for c in x.strip("{}").split(","))

        machines.append(Machine(indicator=indicator, buttons=buttons, joltage=joltage))
    return machines


def tuple_xor(t1: tuple[int, ...], t2: tuple[int, ...]) -> tuple[int, ...]:
    assert len(t1) == len(t2)
    ret: list[int] = []
    for x, y in zip(t1, t2):
        ret.append((x + y) % 2)
    return tuple(ret)


@timer
def get_first_solution(test: bool = False):
    machines = parse_input(test)

    sum_presses = 0

    for machine in machines:
        queue: deque[tuple[tuple[int, ...], int]] = deque()
        seen: set[tuple[int, ...]] = set()

        init_state = tuple(0 for _ in range(len(machine.indicator)))
        seen.add(init_state)
        queue.append((init_state, 0))

        while queue:
            state, n_pressed = queue.popleft()
            if state == machine.indicator:
                sum_presses += n_pressed
                break
            for button in machine.buttons:
                next_state = tuple_xor(state, button)
                if tuple(next_state) not in seen:
                    queue.append((next_state, n_pressed + 1))
                    seen.add(tuple(next_state))
    return sum_presses


@timer
def get_second_solution(test: bool = False):
    machines = parse_input(test)

    sum_presses = 0

    for machine in machines:
        c = np.array([1 for _ in range(len(machine.buttons))])
        A = np.array(machine.buttons).T
        joltage_arr = np.array(machine.joltage)

        constraint = LinearConstraint(A, lb=joltage_arr, ub=joltage_arr)
        bounds = Bounds(0, np.inf)
        res = milp(
            c=c,
            constraints=[constraint],
            bounds=bounds,
            integrality=[1] * len(machine.buttons),
        )

        sum_presses += round(sum(res.x))
    return sum_presses


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
