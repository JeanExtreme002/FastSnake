def gcd(a: int, b: int) -> int:
    """
    Euclidean Algorithm for Greatest Common Divisor (GCD)

    Complexity: O(log(min(a, b)))
    """
    if a == 0:
        return b
    return gcd(b % a, a)