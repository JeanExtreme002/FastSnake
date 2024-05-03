def lcm(a: int, b: int) -> int:
    """
    Euclidean Algorithm for Least Common Multiple (LCM)

    Complexity: O(log(n))
    """
    v = a * b

    while b != 0:
        a, b = b, a % b

    return v // a