# Contains the exhaustive implementation of the Subset Sum decision problem

# Given a set of numbers, return all subset sums
def get_all_subset_sums(nums):
    solution = []
    set_size = len(nums)
    num_subsets = 1 << set_size
    for i in range(1, num_subsets):  # Start from 1 to exclude empty subset
        subset_sum = 0
        for j in range(set_size):
            if i & (1 << j) != 0:
                subset_sum += nums[j]
        solution.append(subset_sum)

    return solution


# Given a set of numbers and a targets value, does there exist a subset whose elements add up to the given targets?
def brute_force_subset_sum(nums, target):
    if target == 0:
        return True
    subset_sums = get_all_subset_sums(nums)
    for x in subset_sums:
        if x == target:
            return True

    return False


# Greedily determines if there exists a subset whose elements add up to the given target. Is not optimal.
def greedy_subset_sum(nums, target):
    A = []
    curr_sum = 0
    nums.sort(reverse=True)
    for num in nums:
        if curr_sum + num > target:
            break
        curr_sum = curr_sum + num
        A.append(num)

    result = (curr_sum == target)

    return result
