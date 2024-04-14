# Problema da Mochila

def knapsack(profit, weight, capacity, n):
    """
    Returns the maximum value that can be put in a knapsack of capacity W.
    
    profit = [60, 100, 120] 
    weight = [10, 20, 30] 
    capacity = 50
    n = len(profit) 
    print(knapSack(profit, weight, capacity, n))
    """
    K = [[0 for x in range(profit + 1)] for x in range(n + 1)] 
 
    # Build table K[][] in bottom up manner 
    for i in range(n + 1): 
        for w in range(profit + 1): 
            if i == 0 or w == 0: 
                K[i][w] = 0
            elif weight[i-1] <= w: 
                K[i][w] = max(capacity[i-1] + K[i-1][w-weight[i-1]], K[i-1][w]) 
            else: 
                K[i][w] = K[i-1][w] 
 
    return K[n][profit] 
