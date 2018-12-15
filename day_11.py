from typing import Tuple, Iterable
from time import time

def hundreds_digit(x: int) -> int:
    return (x % 1000) // 100

def power_level(x: int, y: int, grid_serial_number: int) -> int:
    rack_id = x + 10
    P  = rack_id * y + grid_serial_number
    P *= rack_id
    P  = hundreds_digit(P)
    return P - 5

GSN = 5235

GRID = [
    [power_level(x, y, GSN) for x in range(0, 301)]
    for y in range(0, 301)
]

def neighbors(x: int, y: int, size: int) -> Iterable[Tuple[int, int]]:
    return (
        (x + j, y + i)
        for i in range(size)
        for j in range(size)
    )

def neighbor_power(x: int, y: int, grid_serial_number: int, size: int) -> int:
    return sum(
        # power_level(x=N_x, y=N_y, grid_serial_number=grid_serial_number)
        GRID[N_y][N_x]
        for N_x, N_y in neighbors(x, y, size)
    )

assert power_level(x=3, y=5, grid_serial_number=8) == 4
assert power_level(x=122, y=79, grid_serial_number=57) == -5
assert power_level(x=217, y=196, grid_serial_number=39) == 0
assert power_level(x=101, y=153, grid_serial_number=71) == 4

def part_one(size: int, grid_serial_number: int) -> Tuple[int, Tuple[int,int]]:
    a = time()
    x, y = max(
        ((x,y) for x in range(1, 300 + 2 - size) for y in range(1, 302 - size)),
        key=lambda xy: neighbor_power(xy[0], xy[1], grid_serial_number, size=size)
    )
    R = neighbor_power(x, y, grid_serial_number, size), (x,y)
    print(f'size: {size} {time() - a}', R)
    return R

def part_two(grid_serial_number) -> Tuple[int, Tuple[int,int]]:
    return max(
        range(1,301),
        key=lambda size: part_one(size, grid_serial_number)
    )

# print(part_one(size=3, grid_serial_number=42))
print(part_two(grid_serial_number=18))

# 1 297
