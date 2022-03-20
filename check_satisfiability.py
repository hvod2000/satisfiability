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