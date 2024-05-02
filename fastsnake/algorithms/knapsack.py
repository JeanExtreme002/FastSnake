# Problema da Mochila
# Tempo: O(N * capacity)
# Espaço: O(capacity)

def knapsack(profit: list, weight: list, capacity: int, n = None):
    """
    Returns the maximum value that can be put in a knapsack of capacity W.
    
    profit = [60, 100, 120] 
    weight = [10, 20, 30] 
    capacity = 50
    n = len(profit)
    
    value = knapSack(profit, weight, capacity, n)
    """
    if n is None: n = len(profit)
    
    # Making the dp array 
    dp = [0 for i in range(capacity + 1)] 
 
    # Taking first i elements 
    for i in range(1, n + 1): 
         
        # Starting from back, 
        # so that we also have data of 
        # previous computation when taking i-1 items 
        for w in range(capacity, 0, -1): 
            if weight[i-1] <= w: 
                 
                # Finding the maximum value 
                dp[w] = max(dp[w], dp[w - weight[i-1]] + profit[i-1]) 
     
    # Returning the maximum value of knapsack 
    return dp[capacity]
