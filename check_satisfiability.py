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


def eval(quantifiers, clauses):
    t = time()
    old_clauses, clauses = clauses, set()
    for clause in old_clauses:
        clause = frozenset(clause)
        for v in list(clause):
            if v > 0 and v in clause and -v in clause:
                break
        else:
            clauses.add(tuple(reversed(sorted(clause, key=abs))))
    clause_pool, clause_ptrs, indexes = [None], set(), {}
    for clause in clauses:
        ref = 0
        #print(clause)
        for var in clause:
            node = (var, ref)
            if node not in indexes:
                indexes[node] = len(clause_pool)
                clause_pool.append(node)
            ref = indexes[node]
        clause_ptrs.add(ref)
    #print(clause_pool)
    print(len(clause_pool), len(clause_ptrs))
    print("start after", time() - t)

    def set_value(clauses, var, value):
        old_clauses, clauses = clauses, set()
        for cls in old_clauses:
            next_var, tail = clause_pool[cls]
            if abs(next_var) != abs(var):
                clauses.add(cls)
            elif next_var * value < 0:
                clauses.add(tail)
        return frozenset(clauses)

    @cache
    def dp(clauses):
        if not clauses or 0 in clauses:
            return not clauses
        var = min(abs(clause_pool[cls][0]) for cls in clauses)
        values = (dp(set_value(clauses, var, v)) for v in (-1, 1))
        return all(values) if quantifiers[var - 1] == "A" else any(values)

    return dp(frozenset(clause_ptrs))


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
