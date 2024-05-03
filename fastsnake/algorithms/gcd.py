def gcd(a: int, b: int) -> int:
    """
    Euclidean Algorithm for Greatest Common Divisor (GCD)

    Complexity: O(log(n))
    """
    while b != 0:
        a, b = b, a % b
    return a
