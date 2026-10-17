"""Small-graph exact-input arithmetic bounds on algebraic connectivity.

Fractions represent the supplied binary floating-point weights, not physical
measurement precision. Bounds are diagnostic, not evidence of transmission.
"""
from fractions import Fraction
from math import isfinite


def connectivity_interval(adjacency, *, max_nodes=12):
    """Bound lambda_2 with a maximum-spanning-tree and Rayleigh cut tests.

    For a connected n-node graph, the tree bottleneck w gives
    lambda_2 >= n*w / ((n-1)*floor(n*n/4)).
    Each tree-edge cut S gives lambda_2 <= n*cut(S)/(|S|*(n-|S|)).
    """
    rows = list(adjacency)
    n = len(rows)
    if n == 0 or n > max_nodes or any(len(row) != n for row in rows):
        raise ValueError("nonempty square adjacency within max_nodes required")
    A = []
    for row in rows:
        converted = []
        for x in row:
            if isinstance(x, bool):
                raise ValueError("Boolean weights are not allowed")
            try:
                val = float(x)
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("numeric weights required") from exc
            if not isfinite(val) or val < 0:
                raise ValueError("finite nonnegative weights required")
            converted.append(Fraction.from_float(val))
        A.append(converted)
    for i in range(n):
        if A[i][i] != 0 or any(A[i][j] != A[j][i] for j in range(i)):
            raise ValueError("symmetric zero-diagonal adjacency required")
    if n == 1:
        return {"components": 1, "lower": None, "upper": None,
                "status": "NOT_APPLICABLE"}

    parents = list(range(n))

    def find(x):
        while parents[x] != x:
            parents[x] = parents[parents[x]]
            x = parents[x]
        return x

    edges = sorted(((A[i][j], i, j) for i in range(n)
                    for j in range(i + 1, n) if A[i][j] > 0), reverse=True)
    tree = []
    for weight, i, j in edges:
        a, b = find(i), find(j)
        if a != b:
            parents[a] = b
            tree.append((i, j, weight))
    components = len({find(i) for i in range(n)})
    if components > 1:
        return {"components": components, "lower": Fraction(0),
                "upper": Fraction(0), "status": "EXACT_TOPOLOGICAL_ZERO"}

    bottleneck = min(weight for _, _, weight in tree)
    lower = Fraction(n, (n - 1) * ((n * n) // 4)) * bottleneck
    upper = None
    for remove_i, remove_j, _ in tree:
        seen = {remove_i}
        frontier = [remove_i]
        while frontier:
            node = frontier.pop()
            for u, v, _ in tree:
                if (u == remove_i and v == remove_j) or (u == remove_j and v == remove_i):
                    continue
                other = v if u == node else u if v == node else None
                if other is not None and other not in seen:
                    seen.add(other)
                    frontier.append(other)
        s = len(seen)
        cross = sum((A[i][j] for i in seen for j in range(n) if j not in seen),
                    Fraction(0))
        bound = Fraction(n, s * (n - s)) * cross
        if upper is None or bound < upper:
            upper = bound
    if not (Fraction(0) < lower <= upper):
        raise ArithmeticError("inconsistent spectral interval")
    return {"components": 1, "lower": lower, "upper": upper,
            "status": "BOUNDED_NOT_ESTIMATED", "tree_bottleneck": bottleneck}
