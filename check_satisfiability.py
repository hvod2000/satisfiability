from dataclasses import dataclass
from functools import cache
from time import time


@dataclass(frozen=True)
class QBCNF:
    quantifiers: tuple
    clauses: frozenset

    def set_value(self, var, value):
        clauses = self.clauses
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
        return QBCNF(self.quantifiers, frozenset(new_clauses))

    @cache
    def dp(self, ind):
        qs, clauses = self.quantifiers, self.clauses
        if clauses is None:
            return 0
        if len(clauses) == 0:
            return 1
        q = quantifiers[ind - 1]
        values = (self.set_value(ind, v).dp(ind + 1) for v in range(2))
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
print(QBCNF(quantifiers, clauses).dp(1))
print(time() - t)
