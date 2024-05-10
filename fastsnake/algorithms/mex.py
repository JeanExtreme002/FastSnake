def mex(array):
    """
    The MEX (minimum excluded) of an array is the smallest non-negative integer that 
    does not belong to the array. Example:

    The MEX of [2,2,1] is 0, because 0 does not belong to the array.
    The MEX of [3,1,0,1] is 2, because 0 and 1 belong to the array, but 2 does not.
    The MEX of [0,3,1,2] is 4 because 0, 1, 2 and 3 belong to the array, but 4 does not.
    """
    # Create a dictionary to store the frequency of each element
    freq_map = {}
    
    for num in array:
        freq_map[num] = freq_map.get(num, 0) + 1

    # Initialize MEX to 0
    mex_val = 0

    # Iterate through non-negative integers from 0 to N
    for i in range(len(array) + 1):
        if i not in freq_map:
            mex_val = i
            break

    # Return MEX as the answer
    return mex_val
