from dataclasses import dataclass
from collections import Counter


class Node:

    def __init__(self, val: int, prv=None, nxt=None) -> None:
        self.val = val
        self.nxt = nxt or self
        self.prv = prv or self

    def splice_before(self, val: int):
        new_node = Node(val, prv=self.prv, nxt=self)
        self.prv.next = new_node
        self.prv = new_node

    def splice_after(self, val: int):
        new_node = Node(val, prv=self, nxt=self.nxt)
        self.nxt.prv = new_node
        self.nxt = new_node

    def delete_before(self):
        self.prv.prv.nxt = self
        self.prv = self.prv.prv

    def delete_after(self):
        self.nxt.nxt.prv = self
        self.nxt = self.nxt.nxt

    def __repr__(self):
        return f'{self.prv.val} <- {self.val} -> {self.nxt.val}'


N = Node(0)
N.splice_after(1)



def place_marble(player: int, i: int, N: Node, scores: Counter) -> Node:
    if i % 23 == 0:
        scores[player] += i
        for _ in range(6):
            N = N.prv
        scores[player] += N.prv.val
        N.delete_before()
        return N
    else:
        N.nxt.splice_after(i)
        return N.nxt.nxt

players = 479
P = 2
scores = Counter()
for i in range(2, 71036*100):
    N = place_marble(player=P, i=i, N=N, scores=scores)
    if i % 10**6 == 0:
        print(i, P, N)
    P = (P + 1) % players


print(scores)
print(max(scores.values()))
