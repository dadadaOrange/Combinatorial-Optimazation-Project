import random
import sys
import argparse
import numpy as np
import os


class subset_sum_data:
    def __init__(self, file_name='./determ_data/mazes.npz',
                 max_length=8, range_min=3, range_max=10):
        self.file_name = file_name
        self.range_min = range_min
        self.range_max = range_max
        self.max_length = max_length
        self.fix_lenth = True

    def generate_density_data(self, n, b, num=5):
        """
        Args:
            n (int): length of each instance (even)
            b (int): largest element in the list
            num: number of instances
        Return:
            instance tuple

        """
        if n % 2 != 0:
            raise ValueError('n (%d) needs to be even. ' % n)

        instances = []
        for _ in range(num):
            arr = []

            for x in range(n):
                bits = []
                for i in range(b):
                    bits.append(str(random.randint(0, 1)))
                arr.append(int(''.join(bits), 2))  # convert to int
            instances.append(arr)
            # if max(instances).bit_length()
        targets = []
        for instance in instances:
            t = self.generate_target(instance)
            targets.append(t)

        self.save(instances, targets)

        return instances, targets

    def generate_all(self):
        arr = self.generate_sample(self.max_length)
        t = self.generate_target(arr)
        self.save(arr, t)

    def generate_target(self, array, is_negative=False):
        """

        Given an array, generate a targets number according to a strategy.
        """
        if is_negative:
            random_float = 3.14
            return random_float

        # num = random.randrange(1, len(array))
        num = len(array) // 2
        # print(num)
        target = sum(random.sample(array, num))
        return target

    def generate_sample(self, length):
        """
        Given length, return a array with length, in which numbers in [range_min, range_max]
        """
        RANGE_MIN = self.range_min
        RANGE_MAX = self.range_max

        r_list = []
        for i in range(length):
            r_list.append(random.randrange(RANGE_MIN, RANGE_MAX + 1))
        return r_list

    def save(self, instances, targets):
        directory = os.path.dirname(self.file_name)

        if not os.path.exists(directory):
            print('making folder. ')
            os.makedirs(directory)
        np.savez_compressed(self.file_name, instances, targets)

    def save_z(self, instances, targets):
        directory = os.path.dirname(self.file_name)

        if not os.path.exists(directory):
            print('making folder. ')
            os.makedirs(directory)
        np.save(self.file_name, instances, targets)

    def read(self):

        with np.load(self.file_name) as f:
            arr = f["arr_" + str(0)]
            t = f["arr_" + str(1)]

        print('reading from local array:', arr)
        print('reading from local targets:', t)

    def generate_arrays(self):
        sizes = [10, 3]
        DEST = "./determ_data/"

        for size in sizes:
            path = os.path.join(DEST, '{}.txt'.format(size))
            with open(path, 'w') as f:
                for item in self.generate_sample(size):
                    f.write("%s\n" % item)
