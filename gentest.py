n, m = 10000, 10000
from random import randint, choice

print(n, m)
print("".join(choice("AE") for _ in range(n)))
for _ in range(m):
    row = []
    for u in range(1, n + 1):
        r = randint(1, 3)
        if r == 1:
            row.append(u)
        if r == 2:
            row.append(-u)
    print(" ".join(str(x) for x in row))
