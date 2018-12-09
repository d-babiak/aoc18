'''
#1 @ 49,222: 19x20
#2 @ 162,876: 28x29
#3 @ 28,156: 17x18
#4 @ 673,337: 24x24
#5 @ 213,834: 20x23
#6 @ 675,523: 20x13
#7 @ 97,7: 11x27
#8 @ 92,512: 11x17
#9 @ 507,525: 27x20
#10 @ 47,742: 21x25
'''
import dataclasses
from collections import Counter
from typing import Iterable, Tuple, Dict, Set

lines = [
    '#1 @ 49,222: 19x20',
    '#2 @ 162,876: 28x29',
    '#3 @ 28,156: 17x18',
    '#4 @ 673,337: 24x24',
    '#5 @ 213,834: 20x23',
    '#6 @ 675,523: 20x13',
    '#7 @ 97,7: 11x27',
    '#8 @ 92,512: 11x17',
    '#9 @ 507,525: 27x20',
    '#10 @ 47,742: 21x25',
]


@dataclasses.dataclass
class Rectangle:
    claim_id: str
    x_0: int
    y_0: int
    width: int
    height: int

def rows_of(r: Rectangle) -> Iterable[int]:
    return range(r.x_0, r.x_0 + r.width)

def cols_of(r: Rectangle) -> Iterable[int]:
    return range(r.y_0, r.y_0 + r.height)

def points_of(r: Rectangle) -> Iterable[Tuple[int, int]]:
    return (
        (row, col)
        for row in rows_of(r)
        for col in cols_of(r)
    )


def parse_rectangle(line: str) -> Rectangle:
# '#1 @ 49,222: 19x20'
    claim_id, _, xy, wh = line.strip().split(' ')
    x, y = [int(i) for i in xy[:-1].split(',')]
    w, h = [int(i) for i in wh.split('x')]
    return Rectangle(claim_id=claim_id, x_0=x, y_0=y, width=w, height=h)


Point = Tuple[int, int]
ClaimId = str

def frequencies(rs: Iterable[Rectangle]) -> Tuple[Counter, Set[ClaimId]]:
    counts = Counter()
    claim_by_point: Dict[Point, ClaimId] = {}
    conflicting_claims = set()
    for r in rs:
        for p in points_of(r):
            if p in claim_by_point:
                conflicting_claims.add(r.claim_id)
                conflicting_claims.add(claim_by_point[p])
            else:
                counts[p] += 1
                claim_by_point[p] = r.claim_id
    return counts, conflicting_claims


def num_overlaps(counts: Counter) -> int:
    return sum(1 for n in counts.values() if n >= 2)

def part_one(pathname: str) -> int:
    with open(pathname) as fp:
        rs = [parse_rectangle(line) for line in fp]
    return num_overlaps(frequencies(rs)[0])


def part_two(pathname: str) -> Set[ClaimId]:
    with open(pathname) as fp:
        rs = [parse_rectangle(line) for line in fp]
    _, conflicts = frequencies(rs)
    return {r.claim_id for r in rs} - conflicts

def main():
    print(part_two('d3_input.txt'))
    # eg = [
    # '#1 @ 1,3: 4x4',
    # '#2 @ 3,1: 4x4',
    # '#3 @ 5,5: 2x2',
    # ]
    # eg_rs = list(map(parse_rectangle, eg))
    # _, cc = frequencies(eg_rs)
    # print({ r.claim_id for r in eg_rs} - cc)

if __name__ == '__main__':
    main()
