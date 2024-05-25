from fastsnake.algorithms.longest_common_subsequence import *


def test_longest_common_subsequence():
    assert lcs([], []) == 0
    assert lcs([1], [1]) == 1
    assert lcs(range(100), range(100)) == 100
    assert lcs(range(100), range(80)) == 80
    assert lcs(range(60), range(80)) == 60
    assert lcs([1, -3, 4, 5], [1, -3, 7, 9, 4, 5]) == 4
    assert lcs([1, -3, 7, 9, 4, 5], [1, -3, 4, 5]) == 4
    assert lcs("AGGTAB", "GXTXAYB") == 4
    assert lcs("AAAA", "AAAA") == 4
    assert lcs("AAAA", "AAAAA") == 4
    assert lcs("AABAA", "AAAAA") == 4
    assert lcs("AABAAA", "AAAAA") == 5
