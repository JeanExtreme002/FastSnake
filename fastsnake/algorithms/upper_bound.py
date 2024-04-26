def upper_bound(array, x):
    low, high = 0, len(array) - 1

    while low <= high:

        mid = (high + low) // 2

        if x < array[mid]:
            high = mid - 1

        else:
            low = mid + 1

    low = low - 1

    return -1 if low >= len(array) or low < 0 or array[low] > x else low

