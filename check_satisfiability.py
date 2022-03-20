from functools import cache
from time import time


def set_value(clauses, var, value):
    new_clauses = set()
    for cls in clauses:
        if cls[0] == var or cls[0] == -var:
            sign = (cls[0] > 0) or -1
            old_cls = cls
            cls = None if (sign * ((value > 0) or -1) > 0) else cls[1:]
        if cls == ():
            return None
        if cls is not None:
            new_clauses.add(cls)
    return frozenset(new_clauses)


@cache
def dp(qs, clauses, ind):
    if clauses is None:
        return 0
    if len(clauses) == 0:
        return 1
    q = quantifiers[ind - 1]
    values = (dp(qs, set_value(clauses, ind, v), ind + 1) for v in range(2))
    return all(values) if q == "A" else any(values)


t = time()
n, m = map(int, input().split())
quantifiers = input()
clauses = []
for i in range(m):
    clauses.append(tuple(map(int, input().split())))
clauses = frozenset(cls for cls in clauses if cls)
print(time() - t)
t = time()
print(dp("AE", clauses, 1))
print(time() - t)
