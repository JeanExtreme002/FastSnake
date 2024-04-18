from typing import List, Optional


def input_float() -> float:
    """
    Return an float from input.
    """
    return float(input())


def input_float_array() -> List[float]:
    """
    Return an float array from input.
    """
    return [float(x) for x in input().split()]
 
 
def input_float_matrix(n_rows: int, separator: Optional[str] = None) -> List[List[float]]:
    """
    Return an float matrix from input.
    """
    return [[float(x) for x in input().split(separator)] for _ in range(n_rows)]


def input_int() -> int:
    """
    Return an int from input.
    """
    return int(input())


def input_int_array() -> List[int]:
    """
    Return an int array from input.
    """
    return [int(x) for x in input().split()]
 
 
def input_int_matrix(n_rows: int, separator: Optional[str] = None) -> List[List[int]]:
    """
    Return an int matrix from input.
    """
    return [[int(x) for x in input().split(separator)] for _ in range(n_rows)]
