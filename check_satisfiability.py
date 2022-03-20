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
    old_clauses, clauses = clauses, set()
    for clause in old_clauses:
        clause = set(clause)
        for v in list(clause):
            if v > 0 and v in clause and -v in clause:
                break
        else:
            clauses.add((0, frozenset(clause)))
    clause_tree = []
    for var in range(len(quantifiers), 0, -1):
        old_clauses, clauses, layer = clauses, set(), {(0, 0): 0}
        for ref, clause in old_clauses:
            val = int(var in clause or -(-var in clause))
            if (ref, val) not in layer:
                layer[(ref, val)] = len(layer)
            clauses.add((layer[(ref, val)], frozenset(clause - {var, -var})))
        layer = (v for i, v in sorted((i, v) for v, i in layer.items()))
        clause_tree.append(tuple(layer))
    clause_tree = tuple(reversed(clause_tree))

    def set_value(clauses, var, value):
        old_clauses, clauses = clauses, set()
        for tail, cls_var in (clause_tree[var - 1][cls] for cls in old_clauses):
            if not cls_var:
                clauses.add(tail)
            elif cls_var * var < 0:
                clauses.add(tail)
        return frozenset(clauses)

    @cache
    def dp(var, clauses):
        if not clauses or 0 in clauses:
            return not clauses
        values = (dp(var + 1, set_value(clauses, var, v)) for v in (-1, 1))
        return all(values) if quantifiers[var - 1] == "A" else any(values)

    return dp(1, frozenset(range(1, len(clause_tree[-1]))))


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
