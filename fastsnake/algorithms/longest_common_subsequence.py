from typing import Iterable

# Time Complexity: O(m * n), which remains the same.
# Auxiliary Space: O(m) because the algorithm uses two arrays of size m.
def longest_common_subsequence(array_1: Iterable, array_2: Iterable):
    """
    Given two strings, S1 and S2, the task is to find the length of 
    the Longest Common Subsequence, i.e. longest subsequence present 
    in both of the strings. 

    A longest common subsequence (LCS) is defined as the longest 
    subsequence which is common in all given input sequences.

    Example:

    STRING_1 = AGGTAB
    STRING_2 = GXTXAYB

    LCS = GTAB
    """
    n = len(array_1)
    m = len(array_2)

    # Initializing two lists of size m.
    prev = [0] * (m + 1)
    cur = [0] * (m + 1)

    for idx1 in range(1, n + 1):
        for idx2 in range(1, m + 1):

            # If characters are matching
            if array_1[idx1 - 1] == array_2[idx2 - 1]:
                cur[idx2] = 1 + prev[idx2 - 1]
            else:
                # If characters are not matching
                cur[idx2] = max(cur[idx2 - 1], prev[idx2])

        prev = cur.copy()

    return cur[m]


lcs = longest_common_subsequence