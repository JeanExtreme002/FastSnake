def binary_search(array, x):
    low = 0
    high = len(array) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        # If x is greater, ignore left half
        if array[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif array[mid] > x:
            high = mid - 1

        # means x is present at mid
        else:
            return mid

    # If we reach here, then the element was not present
    return -1

