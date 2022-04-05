n, m = 10000, 10000
from random import randint, choice

print(n, m)
print("".join(choice("AE") for _ in range(n)))
for _ in range(m):
    u = choice(list(range(1, n + 1)))
    v = choice(list(set(range(1, n + 1)) - {u}))
    row = [[x, -x][randint(0, 1)] for x in [u, v]]
    print(" ".join(str(x) for x in row))
