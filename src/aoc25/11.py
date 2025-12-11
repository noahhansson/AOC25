from utils import read_input, timer, setup_args
from functools import cache

args = setup_args()


def parse_input(test: bool = False) -> dict[str, list[str]]:
    inpt = read_input("11", test=test)
    node_connections: dict[str, list[str]] = {}
    for row in inpt:
        node_from, nodes_to = row.split(": ")
        node_connections[node_from] = nodes_to.split(" ")
    return node_connections


def count_paths_to(
    start_node: str,
    target_node: str,
    connections: dict[str, list[str]],
    p2: bool = False,
) -> int:
    @cache
    def _count_paths_to_cache(
        current_node: str,
        target_node: str,
        has_passed_dac: bool = False,
        has_passed_fft: bool = False,
    ):
        if current_node == target_node:
            return has_passed_dac and has_passed_fft
        n_paths = 0
        if current_node == "dac":
            has_passed_dac = True
        if current_node == "fft":
            has_passed_fft = True
        for node in connections[current_node]:
            n_paths += _count_paths_to_cache(
                node, target_node, has_passed_dac, has_passed_fft
            )
        return n_paths

    return _count_paths_to_cache(
        start_node, target_node, has_passed_dac=not p2, has_passed_fft=not p2
    )


@timer
def get_first_solution(test: bool = False):
    node_connections = parse_input(test)

    return count_paths_to("you", "out", node_connections)


@timer
def get_second_solution(test: bool = False):
    node_connections = parse_input(test)

    return count_paths_to("svr", "out", node_connections, p2=True)


print(f"P1: {get_first_solution(test=args.test)}")
print(f"P2: {get_second_solution(test=args.test)}")
