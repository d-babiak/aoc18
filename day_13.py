from collections import Counter
from dataclasses import dataclass
from typing import Dict, Tuple, List, Iterable

X = Y = int

N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)

Direction = Tuple[X, Y]

INTERSECTION = "+"
SE_TURN = "\\"
SW_TURN = "/"


def to_s(dir: Direction) -> str:
    return {
        (0, -1): 'N',
        (0,  1): 'S',
        (1,  0): 'E',
        (-1, 0): 'W',
    }[dir]


def turn_left(d: Direction) -> Direction:
    dirs = {N: W, W: S, S: E, E: N}
    return dirs[d]


def turn_right(d: Direction) -> Direction:
    dirs = {W: N, N: E, E: S, S: W}
    return dirs[d]


@dataclass
class Cart:
    x: int
    y: int
    direction: Direction
    intersection_counts: Counter

    def get_next_cell(self) -> Tuple[X, Y]:
        dx, dy = self.direction
        return self.x + dx, self.y + dy

    def move(self, next_cell: Tuple[X, Y], cell_type):
        x, y = next_cell
        self.x = x
        self.y = y

        if cell_type is INTERSECTION:
            # n = self.intersection_counts[next_cell]
            n = self.intersection_counts['SHARED_COUNT']

            if n % 3 == 0:
                self.direction = turn_left(self.direction)
            elif n % 3 == 1:
                self.direction = self.direction
            elif n % 3 == 2:
                self.direction = turn_right(self.direction)

            self.intersection_counts['SHARED_COUNT'] += 1
            return

        if cell_type is SE_TURN:
            if self.direction in (S, N):
                self.direction = turn_left(self.direction)
            elif self.direction in (E, W):
                self.direction = turn_right(self.direction)
            else:
                raise ValueError("wtf")
            return

        if cell_type is SW_TURN:
            if self.direction in (S, N):
                self.direction = turn_right(self.direction)
            elif self.direction in (E, W):
                self.direction = turn_left(self.direction)
            else:
                raise ValueError("wtf")
            return


CellType = str  # \ / - | +


class Grid:
    cells: Dict[Tuple[X, Y], CellType]
    carts: Dict[Tuple[X, Y], Cart]

    def __init__(self):
        self.cells = {}
        self.carts = {}


    def has_cart(self, xy):
        return xy in self.carts

    def move_cart(self, cart: Cart, next_cell: Tuple[X, Y]):
        self.carts.pop((cart.x, cart.y))
        self.carts[next_cell] = cart

        cart.move(next_cell, cell_type=self.cells[next_cell])

    def print(self):
        max_x = max(xy[0] for xy in self.cells)
        max_y = max(xy[1] for xy in self.cells)
        for y in range(max_y + 1):
            row = [
                to_s(self.carts.get((x, y)).direction) if self.carts.get((x, y)) else self.cells.get((x, y), ' ') # .__.
                for x in range(max_x + 1)
            ]
            row = ''.join(row)
            print(row)

CART_DIRECTIONS = {"<": (W, "-"), "^": (N, "|"), ">": (E, "-"), "v": (S, "|")}


def parse_input(lines: Iterable[str]) -> Tuple[Grid, List[Cart]]:
    grid = Grid()
    carts = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c not in CART_DIRECTIONS:
                grid.cells[(x, y)] = c
                continue
            cart_dir, track_dir = CART_DIRECTIONS[c]
            cart = Cart(x=x, y=y, direction=cart_dir, intersection_counts=Counter())
            carts.append(cart)
            grid.cells[(x, y)] = track_dir
            grid.carts[(x, y)] = cart
    return grid, carts


demo_input = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/  
""".strip()

# demo_input = r'''
# |
# v
# |
# |
# |
# ^
# |
# '''.strip()

def part_one():
    with open('inputs/d13.txt') as fp:
        # lines = demo_input.splitlines()
        lines = fp.read().splitlines()

    grid, carts = parse_input(lines)

    while True:
        carts = sorted(carts, key=lambda c: (c.y, c.x))
        for cart in carts:
            # print('-------------------------------------------------')
            # grid.print()
            next_cell = cart.get_next_cell()

            if grid.has_cart(next_cell):
                print("👹")
                return next_cell

            grid.move_cart(cart, next_cell)
            # grid.print()

if __name__ == '__main__':
    print(part_one())
