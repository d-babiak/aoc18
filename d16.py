from collections import defaultdict
from typing import Dict, Tuple, List

Regs = Dict[int, int]


def I(cond) -> int:
    return 1 if cond else 0

def addr(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A] + rs[B]}

def addi(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A] + B}

def mulr(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A] * rs[B]}

def muli(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A] * B}

def banr(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A] & rs[B]}

def bani(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A] & B}

def borr(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A] | rs[B]}

def bori(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A] | B}

def setr(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: rs[A]}

def seti(rs: Regs, A: int, B: int, C: int) -> Regs:
    return {**rs, C: A}

def gtir(rs: Regs, A: int, B: int, C: int) -> Regs:
    val = I(A > rs[B])
    return {**rs, C: val}

def gtri(rs: Regs, A: int, B: int, C: int) -> Regs:
    val = I(rs[A] > B)
    return {**rs, C: val}

def gtrr(rs: Regs, A: int, B: int, C: int) -> Regs:
    val = I(rs[A] > rs[B])
    return {**rs, C: val}

def eqir(rs: Regs, A: int, B: int, C: int) -> Regs:
    val = I(A == rs[B])
    return {**rs, C: val}

def eqri(rs: Regs, A: int, B: int, C: int) -> Regs:
    val = I(rs[A] == B)
    return {**rs, C: val}

def eqrr(rs: Regs, A: int, B: int, C: int) -> Regs:
    val = I(rs[A] == rs[B])
    return {**rs, C: val}

S = '''
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
'''.strip()

OPS = (
    addr,
    addi,
    mulr,
    muli,
    bori,
    borr,
    banr,
    bani,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
)

def parse_op(s: str) -> Tuple[int]:
    return tuple(int(x) for x in s.split(' '))

def parse_case(s: str):
    if isinstance(s, list):
        s1, s2, s3 = s
    else:
        s1, s2, s3 = s.splitlines()
    # print(s1, s2, s3)
    before = dict(enumerate(int(x) for x in s1[9:-1].split(', ')))
    op = parse_op(s2)
    after = dict(enumerate(int(x) for x in s3[9:-1].split(', ')))
    return before, op, after

def possible_matches(before: Regs, op: Tuple[int], after: Regs) -> List[str]:
    return [f.__name__ for f in OPS if f(before, *list(op)[1:]) == after]

def part_one(pathname) -> int:
    n = 0

    with open(pathname) as fp:
        for _ in range(751):
            s = [next(fp).strip() for _ in range(3)]
            assert s[0].startswith('Before')
            assert s[-1].startswith('After')
            assert not(str(next(fp, '').strip()))
            before, op, after = parse_case(s)
            matches = possible_matches(before, op, after)

            if len(matches) >= 3:
                n += 1

    return n

OP_MAP = {
     0: setr,
     1: eqrr,
     2: gtri,
     3: muli,
     4: eqir,
     5: borr,
     6: bori,
     7: mulr,
     8: gtrr,
     9: seti,
    10: banr,
    11: eqri,
    12: addr,
    13: gtir,
    14: addi,
    15: bani,
}

def reverse_eng(pathname) -> dict:
    ops = defaultdict(set)

    with open(pathname) as fp:
        for _ in range(751):
            s = [next(fp).strip() for _ in range(3)]
            assert s[0].startswith('Before')
            assert s[-1].startswith('After')
            assert not(str(next(fp, '').strip()))
            before, op, after = parse_case(s)
            matches = possible_matches(before, op, after)

            op_code = op[0]
            if op_code in OP_MAP:
                continue
            for f in matches:
                ops[f].add(op[0])

    return ops


def part_two(pathname) -> Dict:
    rs = {0: 0, 1: 0, 2: 0, 3: 0}
    with open(pathname) as fp:
        for line in map(str.strip, fp):
            opcode, A, B, C = [int(x) for x in line.split(' ')]
            f = OP_MAP[opcode]
            rs = f(rs=rs, A=A, B=B, C=C)
    return rs

N = part_one('d16.txt')
print(N)


from pprint import pprint
pprint(part_two('d16-2.txt'))

