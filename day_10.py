import os
import re
from dataclasses import dataclass
from typing import Tuple, List, Optional, Dict

counter = {'point_id': 0}

@dataclass
class Point:
    point_id: int
    position: Tuple[int, int]
    velocity: Tuple[int, int]

    @property
    def x(self) -> int: return self.position[0]

    @property
    def y(self) -> int: return self.position[1]

    @property
    def dx(self) -> int: return self.velocity[0]

    @property
    def dy(self) -> int: return self.velocity[1]

    def step(self, c = 1) -> None:
        self.position = self.x + c*self.dx, self.y + c*self.dy
        # print(self.position)

    def __str__(self): return '#'

    def __repr__(self): return '#'

P = Point(point_id=None, position=(3,9), velocity=(1,-2))

def parse_line(line: str) -> Point:
    x, y, dx, dy = map(int, re.match(
        'position=<([- ]?\d+),\s*([- ]?\d+)> velocity=<([- ]?\d+),\s*([- ]?\d+)>',
        line
    ).groups())
    counter['point_id'] += 1
    return Point(point_id=counter['point_id'], position=(x, y,), velocity=(dx, dy))

def parse_points(pathname: str = './input/d10.txt') -> List[Point]:
    with open(pathname) as fp:
        return [parse_line(line.rstrip()) for line in fp]


def distance(p1: Point, p2: Point) -> int:
    return abs(p2.y - p1.y) + abs(p2.x - p1.x)


def diameter(ps: List[Point]) -> int:
    return max(
        distance(p1, p2)
        for p1 in ps
        for p2 in ps
    )

Grid = List[List[Optional[Point]]]

def empty_grid(dim: int) -> Grid:
    return [
        [None for _ in range(dim)]
        for _ in range(dim)
    ]


def part_one():
    points: List[Point] = parse_points()

    min_X = min(p.x for p in points)
    min_Y = min(p.x for p in points)

    for p in points:
        p.position = (p.x - min_X, p.y - min_Y)

    dim = diameter(points)
    print(f'Diameter: {dim}')

    grid = {}

    for p in points:
        grid[p.position] = p

    i = 0

    for p in points:
        p.step(c=10519)

    min_X = min(p.x for p in points)
    min_Y = min(p.x for p in points)

    for p in points:
        p.position = (p.x - min_X, p.y - min_Y)

    dim = diameter(points)
    print(f'Diameter: {dim}')

    while i < 10**4:
        D = diameter(points)
        print(i, D)

        for p in points:
            p.step()

        if D < 80:
            min_X = min(p.x for p in points)
            min_Y = min(p.x for p in points)
            for p in points:
                p.position = (p.x - min_X, p.y - min_Y)
            print('woot')
            draw(points, D)
            break

        i += 1

    print('wtf')


def draw(points: List[Point], dim: int) -> None:
    G = empty_grid(dim)

    for p in points:
        G[p.y][p.x] = '#'

    for p in points:
        print(p.velocity)

    G = [
        [
            '.' if G[row][col] is None else '#'
            for col in range(dim)
        ]
        for row in range(dim)
    ]
    print()
    for x in G:
        print(' '.join(x))
    print()


if __name__ == '__main__':
    part_one()
