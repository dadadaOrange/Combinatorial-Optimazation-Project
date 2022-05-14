"""
The exhaustive algorithm will find all subset sum in input list. For each subset, check if the subset sum equals to
target.
"""
from timeit import default_timer as timer


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    from itertools import chain, combinations
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def exhaustive_search(l, k):
    for s in powerset(l):
        if sum(s) == k:
            return True
    return False


def test_exhaustive(arrays, t):
    print('array is:', arrays[0])
    print('target is:', t[0])
    start = timer()
    test_instance = arrays[0]
    test_target = t[0]
    res = exhaustive_search(test_instance, test_target)
    print('the result is:', res)
    end = timer()
    return end - start
