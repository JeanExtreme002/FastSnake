# m is size of coins array (number of different coins)
def minCoins(coins, m, value):
    """
    coins = [9, 6, 5, 1]
    m = len(coins)
    value = 11
    print("Minimum coins required is ", minCoins(coins, m, value))
    """
	
    # table[i] will be storing the minimum 
    # number of coins required for i value. 
    # So table[value] will have result
    table = [0 for i in range(value + 1)]

    # Base case (If given value value is 0)
    table[0] = 0

    # Initialize all table values as Infinite
    for i in range(1, value + 1):
        table[i] = float("inf")

    # Compute minimum coins required 
    # for all values from 1 to value
    for i in range(1, value + 1):
            
        # Go through all coins smaller than i
        for j in range(m):
            if (coins[j] <= i):
                sub_res = table[i - coins[j]]
                
                if (sub_res != float("inf") and sub_res + 1 < table[i]):
                    table[i] = sub_res + 1
    
    if table[value] == float("inf"):
        return -1
    
    return int(table[value])

