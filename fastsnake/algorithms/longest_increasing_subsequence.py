# Time Complexity: O(nlog(n))
from typing import List


def longest_increasing_subsequence(array: List[int]):
    """
    Given an array of size N, the task is to find the length 
    of the Longest Increasing Subsequence (LIS) i.e., the longest 
    possible subsequence in which the elements of the subsequence 
    are sorted in increasing order.

    Example 1: For lis([3, 10, 2, 1, 20]), the answer is 3,
    because the longest increasing subsequence is 3, 10, 20.

    Example 2: For lis([1, -1, 3, 3, 3, -6, 5, 7]), the answer is 4,
    because the longest increasing subsequence is 1, 3, 5, 7
    """
    if not array: return 0

    n = len(array)
    ans = []

    # Initialize the answer list with the
    # first element of nums
    ans.append(array[0])

    for i in range(1, n):
        if array[i] > ans[-1]:
            # If the current number is greater
            # than the last element of the answer
            # list, it means we have found a
            # longer increasing subsequence.
            # Hence, we append the current number
            # to the answer list.
            ans.append(array[i])
        else:
            # If the current number is not
            # greater than the last element of
            # the answer list, we perform
            # a binary search to find the smallest
            # element in the answer list that
            # is greater than or equal to the
            # current number.
            low = 0
            high = len(ans) - 1

            while low < high:
                mid = low + (high - low) // 2

                if ans[mid] < array[i]:
                    low = mid + 1
                else:
                    high = mid

            # We update the element at the
            # found position with the current number.
            # By doing this, we are maintaining
            # a sorted order in the answer list.
            ans[low] = array[i]

    # The length of the answer list
    # represents the length of the
    # longest increasing subsequence.
    return len(ans)


lis = longest_increasing_subsequence
