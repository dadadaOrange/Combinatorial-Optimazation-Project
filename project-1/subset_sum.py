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


# Given a set of numbers and a target value, does there exist a subset whose elements add up to the given target?
def brute_force_subset_sum(nums, target):
    if target == 0:
        return True
    subset_sums = get_all_subset_sums(nums)
    for x in subset_sums:
        if x == target:
            return True

    return False
