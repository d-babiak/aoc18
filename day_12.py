# states that transition to a plant
S = {
'#..#.',
'#.#..',
'###..',
'.#.##',
'...#.',
'##.#.',
'###.#',
'####.',
'.##..',
'#.##.',
'#..##',
'##...',
'##.##',
'.#..#',
'..#.#',
'.####',
'..#..',
'.##.#',
}

def chunk_of_5(state: str, i: int) -> str:
    return ''.join(state[j % len(state)] for j in range(i - 2, i + 3))

def next_state(state: str, i: int) -> str:
    chunk = chunk_of_5(state, i)
    return '#' if chunk in S else '.'

Y = '#...#..##.......####.#..###..#.##..########.#.#...#.#...###.#..###.###.#.#..#...#.#..##..#######.##'

# X = ''.join('.' for _ in range(20)) + '#..#.#..##......###...###' + ''.join('.' for _ in range(20))
X = ''.join('.' for _ in range(10)) + Y + ''.join('.' for _ in range(220))

def step(state: str) -> str:
    return ''.join(
        next_state(state, i)
        for i in range(len(state))
    )

print(0, X)
acc = sum(
        i
        for i, x in zip(range(-10, len(X) - 10 + 1), X)
        if x == '#'
    )
for i in range(1, 99):
    X = step(X)
    new_acc = sum(
        i
        for i, x in zip(range(-10, len(X) - 10 + 1), X)
        if x == '#'
    )
    print(i, new_acc - acc, X)
    acc = new_acc

res = sum(
    i
    for i, x in zip(range(-10, len(X) - 10 + 1), X)
    if x == '#'
)
print(res)

# print(11029 + (5*10**10 - 99)*91)
print(11029 + (5*10**10 - 98)*91)
