from string import ascii_lowercase
from typing import List, Dict


def reacts_with(x: str, y: str) -> bool:
    return x and y and ord(x) ^ ord(y) == 0b00100000


def last(xs):
    return xs[-1] if xs else None


def part_one(chars: str) -> str:
    reduced: List[str] = []
    for c in chars:
        if reacts_with(last(reduced), c):
            reduced.pop()
        else:
            reduced.append(c)
    return ''.join(reduced)


def length_of_reduced(chars: str) -> int:
    return len(part_one(chars))


def everything_but(char: str, word: str) -> str:
    excluded = (char.lower(), char.upper())
    return ''.join(c for c in word if c not in excluded)

def part_two(chars: str) -> Dict[str, str]:
    return {
        char: length_of_reduced(everything_but(char, chars))
        for char in ascii_lowercase
    }
