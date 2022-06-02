import numpy as np


class subset_sum_solver:
    def __init__(self, data_path):
        self.data_path = data_path
        self.arrays = None
        self.targets = None

    ############################################################################
    def exhaustive(self):
        if self.arrays is None or self.targets is None:
            raise ValueError('Please read data file.')
        res = []
        for i in range(len(self.targets)):
            res.append(self.exhaustive_search(self.arrays[i], self.targets[i]))
        return res

    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        from itertools import chain, combinations
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    def exhaustive_search(self, arr, t):
        for s in self.powerset(arr):
            if sum(s) == t:
                return True
        return False

    ############################################################################
    def greedy_search(self, arr, t):
        running_sum = 0
        # arr.sort()
        # arr.sort(reverse=True)
        arr = sorted(arr, reverse=True)
        for item in arr:
            if running_sum + item <= t:
                running_sum += item
        if running_sum == t:
            return True
        return False

    def greedy(self):
        if self.arrays is None or self.targets is None:
            raise ValueError('Please read data file.')
        res = []
        for i in range(len(self.targets)):
            res.append(self.greedy_search(self.arrays[i], self.targets[i]))
        return res

    ############################################################################
    def read(self):
        with np.load(self.data_path) as f:
            self.arrays = f["arr_" + str(0)]
            self.targets = f["arr_" + str(1)]
            self.n = len(self.arrays[0])
