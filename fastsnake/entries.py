from typing import List, Optional


def input_char_matrix(n_rows: int) -> List[List[str]]:
    """
    Return a char matrix from input.

    Example (input):
    >>> abcd
    >>> efgh
    >>> ijkl
    >>> mnop

    matrix = [["a", "b", "c", "d"], ["e", "f", "g", "h"], ...]
    """
    return [list(input()) for _ in range(n_rows)]


def input_float() -> float:
    """
    Return an float from input.
    """
    return float(input())


def input_float_array(separator: Optional[str] = " ") -> List[float]:
    """
    Return an float array from input.
    """
    return [float(x) for x in input().split(separator)]
 
 
def input_float_matrix(n_rows: int, separator: Optional[str] = " ") -> List[List[float]]:
    """
    Return an float matrix from input.
    """
    return [[float(x) for x in input().split(separator)] for _ in range(n_rows)]


def input_int() -> int:
    """
    Return an int from input.
    """
    return int(input())


def input_int_array(separator: Optional[str] = " ") -> List[int]:
    """
    Return an int array from input.
    """
    return [int(x) for x in input().split(separator)]
 
 
def input_int_matrix(n_rows: int, separator: Optional[str] = " ") -> List[List[int]]:
    """
    Return an int matrix from input.
    """
    return [[int(x) for x in input().split(separator)] for _ in range(n_rows)]


def input_string_matrix(n_rows: int, separator: Optional[str] = " ") -> List[List[str]]:
    """
    Return a string matrix from input.
    """
    return [input().split(separator) for _ in range(n_rows)]
