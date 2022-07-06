import numpy as np
import random
from timeit import default_timer as timer


class subset_sum_solver:
    def __init__(self, data_path, itr_max=1000, time_limit=60, tolerance=500):
        self.data_path = data_path
        self.itr_max = itr_max
        self.time_limit = time_limit
        self.tolerance = tolerance
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

    def greedy_1_approximate(self, arr, t):
        chose_set = []
        running_sum = 0
        arr = sorted(arr, reverse=True)
        for item in arr:
            if running_sum + item <= t:
                running_sum += item
                chose_set.append(item)
        if running_sum == t:
            return True, 0, 1, chose_set
        return False, abs(running_sum - t), running_sum / t, chose_set

    def greedy_5_approximate(self):
        if self.arrays is None or self.targets is None:
            raise ValueError('Please read data file.')
        res = []
        residue = []
        ratio = []
        chose_set = []
        for i in range(len(self.targets)):
            result, resi, rat, chose = self.greedy_1_approximate(self.arrays[i], self.targets[i])
            res.append(result)
            residue.append(resi)
            ratio.append(rat)
            chose_set.append(chose)
        # return res, residue, ratio, chose_set
        return chose_set

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
            return True, running_sum / t
        return False, running_sum / t

    def find_neighbor(self, instance, subset):
        l = instance
        s = subset

        t = s[:]

        l_set = set(l)
        l_set_list = list(l_set)

        i_set, j_set = random.sample(range(0, len(l_set_list)), 2)

        l_i = l_set_list[i_set]
        l_j = l_set_list[j_set]

        if (l_i in s):
            t.remove(l_i)

        else:
            t.append(l_i)

        if (l_j in s):
            if (random.random() < 0.5):
                t.remove(l_j)

        else:
            if (random.random() < 0.5):
                t.append(l_j)

        return t

    def residue(self, s, t):
        total = sum(s)
        return abs(total - t)

    def steepest(self, instance, target, initial_subset):
        if target == 0:
            return

        eps = target / self.tolerance
        # print('eps:', eps)
        count = 0
        current = initial_subset
        cur_gap = self.residue(current, target)

        start = timer()

        while count < self.itr_max:  # member variable
            new = self.find_neighbor(instance, current)
            new_gap = self.residue(new, target)
            if new_gap < cur_gap:
                current = new
                cur_gap = new_gap
            count += 1

            end = timer()
            run_time = end - start
            if cur_gap <= eps:
                print('reach the tolerance')
                break

            if run_time >= self.time_limit:
                print('time out.........')
                break

        return cur_gap, current, run_time, count

    def simulated_annealing(self, instance, target, initial_subset):
        # l: array instance
        # k: target
        # max_itr

        l = instance
        k = target

        max_threshold = self.itr_max
        eps = target / self.tolerance
        start = timer()

        if (k == 0):
            return

        count = 0
        # current = random.sample(l, random.randrange(1, len(l)))
        current = initial_subset
        smallest_residue = self.residue(current, k)
        smallest_subset = current

        while count < max_threshold:

            neighbor = self.find_neighbor(l, current)

            if (self.residue(neighbor, k) < self.residue(current, k)):
                current = neighbor

            else:
                # prob = (self.residue(neighbor, k) - self.residue(current, k)) / (10000000000 * (0.8 ** (count / 300)))
                prob = (self.residue(neighbor, k) - self.residue(current, k)) / (10000000000 * (0.9 ** (count / 300)))
                if (random.random() < prob):
                    current = neighbor

            cur_r = self.residue(current, k)
            if (cur_r < smallest_residue):
                smallest_residue = cur_r
                smallest_subset = current

            end = timer()
            run_time = end - start

            if smallest_residue <= eps:
                print('reach the tolerance.')
                break

            if run_time >= self.time_limit:
                print('time out.........')
                break

            count += 1

        return smallest_residue, smallest_subset, run_time, count

    def greedy(self):
        if self.arrays is None or self.targets is None:
            raise ValueError('Please read data file.')
        res = []
        ratios = []
        for i in range(len(self.targets)):
            res_single, ratio = self.greedy_search(self.arrays[i], self.targets[i])
            res.append(res_single)
            ratios.append(ratio)
        return res, ratios

    ############################################################################
    def read(self):
        with np.load(self.data_path) as f:
            self.arrays = f["arr_" + str(0)]
            self.targets = f["arr_" + str(1)]
            self.n = len(self.arrays[0])
