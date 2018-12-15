from collections import defaultdict, deque, Counter
from itertools import chain
from pprint import pprint
from typing import List, Tuple, Set, Dict, Iterable

Matrix = List[List]
Point = Tuple[int, int]


def marked_matrix(points: Dict[str, Point]) -> Matrix:
    xs, ys = zip(*points.values())
    dim = max(max(xs), max(ys)) + 1
    M = [
        [None for _ in range(dim)]
        for _ in range(dim)
    ]
    mark_all(points, M)
    return M


def mark_all(points: Dict[str, Point], M: Matrix) -> None:
    for p, xy in points.items():
        mark(p, xy, M)


def mark(point_id: str, xy: Point, M: Matrix) -> None:
    col, row = xy
    M[row][col] = point_id


def parse_points(xys: List[Point]) -> Dict[str, Point]:
    return {
        f'P_{i}': coords
        for i, coords in enumerate(xys)
    }





def infinite_points(points: Dict[str, Point]) -> Set[Point]:
    xs, ys = zip(*points.values())

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    return  {
        point_id
        for point_id, (x, y) in points.items()
        if not (x_min < x < x_max) or not (y_min < y < y_max)
    }

U = (0, -1)
D = (0,  1)
L = (-1, 0)
R = ( 1, 0)

DELTAS = frozenset({U, D, L, R})

def in_bounds(xy: Point, M: Matrix) -> bool:
    x, y = xy
    return 0 <= x < len(M) and 0 <= y < len(M)

def neighbors(xy: Point, M: Matrix) -> Iterable[Point]:
    x, y = xy
    return [
        (x + dx, y + dy)
        for dx, dy in DELTAS
        if in_bounds((x + dx, y + dy), M) and M[y + dy][x + dx] is None
    ]


def has_empty_cell(M: Matrix) -> bool:
    return any(cell is None for row in M for cell in row)

def num_none(M: Matrix) -> int:
    return sum(1 for row in M for cell in row if cell is None)

TIED = '.'


# lol
def bfs_flood(PS: Dict[str, Point], M: Matrix) -> Tuple[Matrix, Dict]:
    frontier_by_id = {
        p: [xy]
        for p, xy in PS.items()
    }
    current_epoch = 0
    epoch_by_cell = {}

    while has_empty_cell(M):
        pprint(M)
        next_frontiers = {}
        for p, frontier in frontier_by_id.items():
            next_frontier = []
            for fc, fr in frontier:
                for col, row in neighbors((fc,fr), M): # LOL
                    if M[row][col] is not None and M[row][col] != p and epoch_by_cell[(col,row)] == current_epoch:
                        M[row][col] = TIED
                    elif M[row][col] is None:
                        M[row][col] = p
                        epoch_by_cell[(col,row)] = current_epoch
                        next_frontier.append((col,row))
            next_frontiers[p] = next_frontier
        frontier_by_id = next_frontiers

    return M

# PS = dict(
#     A = (1, 1),
#     B = (1, 6),
#     C = (8, 3),
#     D = (3, 4),
#     E = (5, 5),
#     F = (8, 9)
# )


def parse_grid():
    with open('./input/d6.txt') as fp:
        points = [
            tuple(map(int, line.rstrip().split(',')))
            for line in fp
        ]
    return dict(enumerate(points))

PS = parse_grid()

marked_M = marked_matrix(PS)

def distance(p1, p2) -> int:
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return abs(dx) + abs(dy)

def closest_point(point: Tuple[int,int], points: List[Tuple[str, Tuple[int, int]]]) -> str:
    min_D = min(
        distance(point, p[1]) for p in points
    )
    closest_points = [p for p in points if distance(point, p[1]) == min_D]
    if len(closest_points) > 1:
        print('TIED!', closest_points)
        return '.'
    else:
        print(f'closest point to {point} is  {closest_points[0]}')
        return closest_points[0][0]

for x in marked_M:
    print(' '.join('-' if cell is None else str(cell) for cell in x))

points = list(PS.items())
print(closest_point((4,6), points))

for row in range(len(marked_M)):
    for col in range(len(marked_M[0])):
        if marked_M[row][col] is None:
            marked_M[row][col] = closest_point((col,row), points)

for x in marked_M:
    print(' '.join('-' if cell is None else str(cell) for cell in x))

C = Counter(chain(*marked_M))
S = set(marked_M[0])  | \
    set(marked_M[-1]) | \
    set(row[0] for row in marked_M) | \
    set(row[-1] for row in marked_M)

print(S)
print(C)
for x in S:
    C.pop(x)
print(C)
# finite_points: Set[str] = set(PS.keys()) - infinite_points(PS)

#
# pprint(marked_M)

def part_two(points: List[Tuple[int,int]]) -> int:
    xs, ys = zip(*points)
    dim = max(max(xs), max(ys)) + 1
    return sum(
        1
        for x in range(dim)
        for y in range(dim)
        if sum(distance((x,y), p) for p in points) < 10000
    )
print(part_two(list(PS.values())))
