from utils import read_input, timer, setup_args
import re

args = setup_args()


class Present:
    shape: frozenset[tuple[int, int]]
    rotations: set[Present] | None

    def __init__(self, shape: set[tuple[int, int]]):
        self.shape = frozenset(shape)
        self.xmax = max([s[0] for s in self.shape])
        self.ymax = max([s[1] for s in self.shape])
        self.rotations = None

    def _flip_horizontal(self) -> Present:
        new_shapes = {(s[0], self.ymax - s[1]) for s in self.shape}
        return Present(new_shapes)

    def _flip_vertical(self) -> Present:
        new_shapes = {(self.xmax - s[0], s[1]) for s in self.shape}
        return Present(new_shapes)

    def _rotate_90(self) -> Present:
        new_shapes = set()
        for x, y in self.shape:
            new_shapes.add((-y + self.ymax, x))
        return Present(new_shapes)

    def get_all_rotations(self) -> set[Present]:
        if self.rotations is not None:
            return self.rotations
        rotations: set[Present] = set()
        for rot in (
            self,
            self._rotate_90(),
            self._rotate_90()._rotate_90(),
            self._rotate_90()._rotate_90()._rotate_90(),
        ):
            rotations.add(rot)
            rotations.add(rot._flip_horizontal())
            rotations.add(rot._flip_vertical())

        self.rotations = rotations
        return rotations

    def __eq__(self, other):
        return hash(self.shape) == hash(other.shape)

    def __hash__(self):
        return hash(self.shape)

    def __repr__(self) -> str:
        return "\n".join(
            [
                "".join(
                    ["#" if (x, y) in self.shape else "." for x in range(self.xmax + 1)]
                )
                for y in range(self.ymax + 1)
            ]
        )


class Region:
    size: tuple[int, int]
    occupied: set[tuple[int, int]]

    def __init__(self, size: tuple[int, int], occupied: set[tuple[int, int]] = set()):
        self.size = size
        self.occupied = occupied

    def fit_present(self, present: Present, p: tuple[int, int]) -> Region | None:
        if not self.can_fit(present, p):
            return None
        else:
            return Region(
                self.size,
                set(self.occupied) | {(x + p[0], y + p[1]) for (x, y) in present.shape},
            )

    def can_fit(self, present: Present, p: tuple[int, int]) -> bool:
        present_spots = {(x + p[0], y + p[1]) for (x, y) in present.shape}
        for x, y in present_spots:
            if ((x, y) in self.occupied) or (x >= self.size[0]) or (y >= self.size[1]):
                return False

        return True

    def __repr__(self) -> str:
        return "\n".join(
            [
                "".join(
                    [
                        "#" if (x, y) in self.occupied else "."
                        for x in range(self.size[0])
                    ]
                )
                for y in range(self.size[1])
            ]
        )


def parse_input(test: bool = False):
    inpt = read_input("12", test=test)
    presents: list[Present] = []
    regions: list[tuple[Region, list[int]]] = []
    buffer: set[tuple[int, int]] = set()
    buffer_start_idx = 0
    for i, row in enumerate(inpt):
        if len(re.findall(r"\b\d+:(?!\d)", row)) > 0:
            buffer_start_idx = i + 1
        elif "x" in row:
            size = tuple(map(int, re.findall(r"(\d+)x(\d+):", row)[0]))
            required_presents = list(map(int, row.split()[1:]))
            regions.append((Region((size[0], size[1])), required_presents))
        elif row == "":
            presents.append(Present(buffer))
            buffer = set()
        elif "#" in row:
            for x, c in enumerate(row):
                if c == "#":
                    buffer.add((x, i - buffer_start_idx))

    return presents, regions


def solve(
    region: Region, presents: list[Present], required: list[int], current: list[int]
) -> bool:
    if required == current:
        return True
    for i, (n_req, curr) in enumerate(zip(required, current)):
        if n_req <= curr:
            continue
        next_current = current.copy()
        next_current[i] += 1

        for x in range(region.size[0] - 2):
            for y in range(region.size[1] - 2):
                if (x, y) not in region.occupied:
                    for p in presents[i].get_all_rotations():
                        if (next_region := region.fit_present(p, (x, y))) is not None:
                            if solve(next_region, presents, required, next_current):
                                print("")
                                print(next_region)
                                return True
        return False
    return False


@timer
def get_first_solution(test: bool = False):
    presents, regions = parse_input(test)
    s = 0
    for region, required in regions:
        # Check if there is enough space
        total_size = region.size[0] * region.size[1]
        total_required = sum(len(presents[i].shape) * n for i, n in enumerate(required))
        if total_required > total_size:
            s += 0
        # Check if there is abundant space
        elif (region.size[0] // 3) * (region.size[1] // 3) >= sum(required):
            s += 1
        else:
            # Never happens in real input, only test
            # Takes forever to converge
            s += solve(region, presents, required, [0 for _ in range(len(required))])

    return s


print(f"P1: {get_first_solution(test=args.test)}")
