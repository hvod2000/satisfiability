n, m = 10000, 10000
from random import randint, choice

print(n, m)
print("".join(choice("AE") for _ in range(n)))
for _ in range(m):
    row = []
    for u in (randint(1, n), randint(1, n)):
        row.append([u, -u][randint(0, 1)])
    print(" ".join(str(x) for x in row))
