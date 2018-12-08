from collections import Counter
from functools import partial
from typing import List, Tuple


def has_k_duplicates(counts: Counter, k: int) -> bool:
    return k in counts.values()

has_two_duplicates   = partial(has_k_duplicates, k=2)

has_three_duplicates = partial(has_k_duplicates, k=3)

def checksum(xs: List[str]) -> int:
    counts = list(map(Counter, xs))
    num_with_two   = sum(1 for x in counts if has_two_duplicates(x))
    num_with_three = sum(1 for x in counts if has_three_duplicates(x))
    return num_with_two * num_with_three


def part_two(ids: List[str]) -> Tuple[str, str]:
    for i in range(len(ids) - 1):
        for j in range(i + 1, len(ids)):
            id_1 = ids[i]
            id_2 = ids[j]
            if exactly_one_difference(id_1, id_2):
                return id_1, id_2

def exactly_one_difference(w1, w2) -> bool:
    return number_of_differences(w1, w2) == 1

def number_of_differences(w1, w2) -> int:
    return sum(
        1
        for x, y in zip(w1, w2)
        if x != y
    )


def parse_ids(pathname) -> List[str]:
    with open(pathname) as fp:
        return [line.strip() for line in fp]

xs = [
    'abcdef',
    'bababc',
    'abbcde',
    'abcccd',
    'aabcdd',
    'abcdee',
    'ababab'
]

zs = [
    'abcde',
    'fghij',
    'klmno',
    'pqrst',
    'fguij',
    'axcye',
    'wvxyz',
]

# if __name__ == '__main__':
#     ids = parse_ids('d2_input.txt')
#     z = checksum(ids)
#     print(z)
#

# if __name__ == '__main__':
#     a, b = part_two(zs)
#     print()

if __name__ == '__main__':
    ids = parse_ids('d2_input.txt')
    print(part_two(ids))
