import heapq
import re
from collections import defaultdict
from pprint import pprint
from typing import List, Dict, Tuple
from itertools import chain


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


def parse_graph(pathname: str = 'd7.txt') -> Graph:
    G = defaultdict(list)
    with open(pathname) as fp:
        for line in fp:
            U, D = parse_line(line.rstrip())
            G[U].append(D)
    NS = set(G.keys()).union(*chain(G.values()))

    for N in NS:
        if N not in G:
            G[N] = []
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
            if incomplete_dependencies(N=child, G=G, C=ordered) or child in seen:
                continue
            heapq.heappush(frontier, child)
            seen.add(child)

    return ordered


TimeElapsed = int


def time_for_task(x: str) -> int:
    return ord(x) - 4# - 60


def increment_times(elapsed_time_by_task: Dict[Node, TimeElapsed]) -> None:
    for k in elapsed_time_by_task:
        elapsed_time_by_task[k] += 1


def visualize(G: Graph) -> str:
    edges =' '.join(
        f'{k} -> {v};'
        for k, vs in G.items()
        for v in vs
    )
    return f'''
digraph G {
{edges}
}    
    '''

'''
digraph G {P -> F; P -> Z; P -> K; P -> X; P -> L; P -> R; P -> M; P -> I; F -> M; F -> N; F -> E; F -> T; Q -> S; Q -> I; Q -> H; Q -> R; Q -> D; K -> G; K -> Y; K -> O; K -> L; K -> B; W -> X; W -> A; W -> V; W -> S; W -> H; W -> J; V -> I; V -> O; V -> Z; V -> H; V -> U; V -> A; S -> Y; S -> Z; S -> X; S -> M; S -> H; S -> N; U -> D; U -> Z; J -> B; J -> O; J -> X; J -> H; J -> L; Z -> C; Z -> A; Z -> L; Y -> D; Y -> L; Y -> C; Y -> O; X -> A; X -> I; X -> C; X -> M; X -> E; X -> R; X -> H; X -> T; E -> N; E -> H; E -> D; E -> R; M -> B; M -> L; M -> R; M -> A; N -> I; N -> A; N -> L; N -> G; I -> T; I -> H; H -> A; H -> L; H -> G; H -> B; H -> C; H -> O; H -> R; A -> B; A -> R; O -> L; O -> R; O -> B; T -> L; T -> B; D -> R; D -> L; G -> L; G -> R; G -> B; G -> C; C -> R; C -> B; R -> L; R -> B; L -> B;} 
'''

def task_sim(G: Graph, max_workers: int = 1) -> TimeElapsed:
    complete = set()
    elapsed_time_by_task: Dict[Node, TimeElapsed] = {}
    valid_tasks: List[Node] = [N for N in G if not incomplete_dependencies(N, G, C=[])]
    seen = set()
    workers_available = max_workers
    i = 0

    while len(complete) < len(G):
        assert workers_available >= 0, 'wtf'
        assert workers_available <= max_workers, 'wtf2'
        assert len(elapsed_time_by_task) == max_workers - workers_available, 'wtf3'

        completed: List[str] = [
            task
            for task, time_elapsed in elapsed_time_by_task.items()
            if time_for_task(task) == time_elapsed
        ]

        for T in completed:
            elapsed_time_by_task.pop(T)
            complete.add(T)
            workers_available += 1
            print(f'Done with {T}')

            if len(complete) == len(G):
                print('Done!')
                return i

        # schedule next tasks
            for child in G[T]:
                U = incomplete_dependencies(N=child, G=G, C=complete)
                if U:
                    print(f'Cant schedule {child}')
                    continue
                if child in seen:
                    print(f'Already seen {child}')
                    continue
                heapq.heappush(valid_tasks, child)
                seen.add(child)

        while workers_available and valid_tasks:
            next_task = heapq.heappop(valid_tasks)
            print(f'Starting work on {next_task}, it requires {time_for_task(next_task)}')
            elapsed_time_by_task[next_task] = 0
            workers_available -= 1

        print(i, elapsed_time_by_task)
        increment_times(elapsed_time_by_task)
        i += 1

    return i


# print(priority_order(G))
G = parse_graph()
print(task_sim(G, max_workers=5))
