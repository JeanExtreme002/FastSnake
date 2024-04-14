
# Function to find the MEX of the array
def mex(array):
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


