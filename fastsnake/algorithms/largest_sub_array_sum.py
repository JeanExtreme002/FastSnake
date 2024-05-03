from math import inf

maxint = inf


def max_sub_array_sum(array):
	"""
	Find the sum of contiguous subarray within a one-dimensional 
	array of numbers that has the largest sum.
	"""
	max_so_far = -maxint - 1
	max_ending_here = 0
	
	for i in range(len(array)):
		max_ending_here = max_ending_here + array[i]

		if (max_so_far < max_ending_here):
			max_so_far = max_ending_here

		if max_ending_here < 0:
			max_ending_here = 0

	return max_so_far