# Entry point to running the brute-force Subset Sum algorithm

from subset_sum import brute_force_subset_sum


if __name__ == '__main__':
    success = brute_force_subset_sum([0, 1, 2, 3, 4, 5], 10)
    fail = brute_force_subset_sum([10, 15, 2, 5, 19], -6)
    print(f'Expected success, returned: {success}')
    print(f'Expected fail, returned: {fail}')
