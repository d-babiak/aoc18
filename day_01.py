import sys
from typing import List
from collections import Counter

def part_one(pathname) -> int:
    return sum(parse_frequencies(pathname))

def part_two(pathname: str) -> int:
    frequencies: List[int] = parse_frequencies(pathname)
    acc = 0
    counts = Counter()

    while True:
        for freq in frequencies:
            acc += freq
            counts[acc] += 1

            if counts[acc] >= 2:
                return acc

def parse_frequencies(pathname: str) -> List[int]:
    with open(pathname) as fp:
        numbers = (int(line.strip()) for line in fp)
        return list(numbers)

def main():
    pathname = sys.argv[1]
    part_one(pathname)

print(part_two('d1_input.txt'))
