from utils import read_input, timer, setup_args
from collections import deque

args = setup_args()

def parse_input(test: bool = False):
    inpt = read_input("10", test=test)
    machines: list[dict[str, tuple[int, ...] | list[tuple[int, ...]]]] = []
    for row in inpt:
        machine: dict[str, tuple[int, ...] | list[tuple[int, ...]]] = {}
        machine["buttons"] = []
        for x in row.split(" "):
            if x.startswith("["):
                machine["indicator"] = tuple(1 if c=="#" else 0 for c in x.strip("[]"))
            if x.startswith("("):
                machine["buttons"].append(tuple(int(c) for c in x.strip("()").split(",")))
            if x.startswith("{"):
                machine["joltage"] = tuple(int(c) for c in x.strip("{}").split(","))

        machines.append(machine)
    return machines

def tuple_xor(t1: tuple[int, ...], t2: tuple[int, ...]) -> tuple[int, ...]:
    assert len(t1) == len(t2)
    ret:list[int] = []
    for x, y in zip(t1, t2):
        ret.append((x + y) % 2)
    return tuple(ret)

def tuple_sum(t1: tuple[int, ...], t2: tuple[int, ...]) -> tuple[int, ...]:
    assert len(t1) == len(t2)
    ret:list[int] = []
    for x, y in zip(t1, t2):
        ret.append((x + y))
    return tuple(ret)

@timer
def get_first_solution(test: bool = False):
    machines = parse_input(test)

    sum_presses = 0

    for machine in machines:
        indicator: tuple[int, ...] = machine["indicator"]
        buttons: list[tuple[int, ...]] = machine["buttons"]

        queue: deque[tuple[tuple[int, ...], list[int]]] = deque()
        seen: set[tuple[int, ...]] = set()
        
        init_state = tuple(0 for _ in range(len(indicator)))
        pressed = [0 for _ in range(len(buttons))]

        seen.add(tuple(pressed))
        queue.append((init_state, pressed))

        while queue:
            state, pressed = queue.popleft()
            if state == indicator:
                sum_presses += sum(pressed)
                break
            for i, button in enumerate(buttons):
                next_pressed = pressed.copy()
                next_pressed[i] += 1
                if tuple(next_pressed) not in seen:
                    state_change = tuple([1 if j in button else 0 for j, _ in enumerate(range(len(state)))])
                    next_state = tuple_xor(state, state_change)
                    queue.append((next_state, next_pressed))
                    seen.add(tuple(next_pressed))
    return sum_presses


@timer
def get_second_solution(test: bool = False):
    machines = parse_input(test)

    sum_presses = 0

    for machine in machines:
        joltage: tuple[int, ...] = machine["joltage"]
        buttons: list[tuple[int, ...]] = machine["buttons"]

        queue: deque[tuple[tuple[int, ...], list[int]]] = deque()
        seen: set[tuple[int, ...]] = set()
        
        init_state = tuple(0 for _ in range(len(joltage)))
        pressed = [0 for _ in range(len(buttons))]

        seen.add(tuple(pressed))
        queue.append((init_state, pressed))

        while queue:
            state, pressed = queue.popleft()
            if state == joltage:
                print(state, pressed)
                sum_presses += sum(pressed)
                break
            for i, button in enumerate(buttons):
                next_pressed = pressed.copy()
                next_pressed[i] += 1
                if tuple(next_pressed) not in seen:
                    state_change = tuple([1 if j in button else 0 for j, _ in enumerate(range(len(state)))])
                    next_state = tuple_sum(state, state_change)
                    if any([s > j for s, j in zip(next_state, joltage)]):
                        continue
                    queue.append((next_state, next_pressed))
                    seen.add(tuple(next_pressed))
    return sum_presses


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
