import heapq
import re
from collections import defaultdict
from typing import List, Dict, Tuple

'''
  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
'''

Node = str
Graph = Dict[Node, List[Node]]

G: Graph  = dict(
    C = ['A', 'F'],
    A = ['B', 'D'],
    F = ['E'],
    B = ['E'],
    D = ['E'],
    E = []
)


def dependencies(N: Node, G: Graph) -> List[Node]:
    return [k for k, v in G.items() if N in v]


def incomplete_dependencies(N: Node, G: Graph, C: List[Node]) -> List[Node]:
    return [D for D in dependencies(N, G) if D not in C]


def root_of(G: Graph) -> Node:
    return next(
        N
        for N in G
        if not dependencies(N, G)
    )


def groupby(xs, f) -> Dict[any, List]:
    acc = defaultdict(list)
    for x in xs:
        acc[f(x)].append(x)
    return acc


def parse_graph(pathname: str) -> Graph:
    G = defaultdict(list)
    with open(pathname) as fp:
        for line in fp:
            U, D = parse_line(line.rstrip())
            G[U].append(D)
    return G


def parse_line(line: str) -> Tuple[Node, Node]:
    return re.match(
        '^Step ([A-Z]) must be finished before step ([A-Z]) can begin.$',
        line
    ).groups()


def priority_order(G: Graph) -> List[Node]:
    ordered: List[Node] = []

    frontier: List[Node] = [N for N in G if not incomplete_dependencies(N, G, C=[])]

    seen = set()

    while frontier:
        next_most_important: Node = heapq.heappop(frontier)
        print('popped!', next_most_important)
        ordered.append(next_most_important)

        for child in G[next_most_important]:
            if incomplete_dependencies(N=child, G=G, C=ordered):
                continue

            if child in seen:
                continue

            heapq.heappush(frontier, child)
            seen.add(child)

    return ordered

print(priority_order(G))
