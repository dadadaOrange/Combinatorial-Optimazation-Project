import random
import os


def generate_list(list_size, range_min, range_max):
    """
    Given size, randomly generate a list in [range_min, range_max].
    :param list_size: the size of the list
    :param range_min: minimum range
    :param range_max: maximum range
    :return: list of integers
    """
    RANGE_MIN = range_min
    RANGE_MAX = range_max

    instance_list = []
    for i in range(list_size):
        instance_list.append(random.randrange(RANGE_MIN, RANGE_MAX + 1))
    return instance_list


def save_list(sizes, range_min, range_max):
    """
    Save multiple lists into .txt files such that each list saves into one file
    :param sizes: the number of lists will be saved
    :param range_min: minimum range
    :param range_max: maximum range
    """
    DEST = "../data/"
    for size in sizes:
        path = os.path.join(DEST, '{}.txt'.format(size))
        with open(path, 'w') as f:
            for item in generate_list(size, range_min, range_max):
                f.write("%s\n" % item)
