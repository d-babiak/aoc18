from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Node:
    children: List  # List[Node]
    metadata: List[int]

def parse_node(tokens: List[int], i: int = 0) -> Tuple[Node, int]:
    n_children = tokens[i]
    n_meta = tokens[i + 1]
    j = i + 2
    children = []
    for _ in range(n_children):
        node, j = parse_node(tokens, j)
        children.append(node)
    metadata = tokens[j : j + n_meta]
    return Node(children=children, metadata=metadata), j + n_meta


def tokenize(s: str) -> List[int]:
    return [int(x) for x in s.split(' ')]


def checksum(N: Node) -> int:
    if not N.children:
        return sum(N.metadata)
    else:
        return sum(
            checksum(N.children[i - 1])
            for i in N.metadata
            if 0 <= i - 1 < len(N.children)
        )


def reduce_tree(N: Node) -> int:
    return sum(reduce_tree(c) for c in N.children) + sum(N.metadata)

def part_one(pathname: str = 'd8.txt') -> None:
    with open(pathname) as fp:
        line: str = next(fp).strip()
        tokens: List[int] = tokenize(line)
        root, _ = parse_node(tokens)
        print(reduce_tree(root))

def part_two(pathname: str = 'd8.txt') -> None:
    with open(pathname) as fp:
        line: str = next(fp).strip()
        tokens: List[int] = tokenize(line)
        root, _ = parse_node(tokens)
        print(checksum(root))


S = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
TS = tokenize(S)
print(TS)
N, i = parse_node(TS)
print(checksum(N))
