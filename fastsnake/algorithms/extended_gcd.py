def extended_gcd(a: int, b: int) -> tuple[int]:
    """
    Extended Euclidean Algorithm for Greatest Common Divisor (GCD)

    This algorithm also finds integer coefficients x and y such that: ax + by = gcd(a, b) 

    Complexity: O(log(n))
    """
    x, y, u, v = 0, 1, 1, 0

    while a != 0:
        q, r = b // a, b % a

        m = x - u * q
        n = y - v * q

        b, a, x, y, u, v = a, r, u, v, m, n
        
    gcd = b

    return gcd, x, y