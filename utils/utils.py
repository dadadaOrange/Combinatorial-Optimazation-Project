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


def construct_lists(path):
    result_lists = []
    with open(path, 'r') as f:
        contents = f.readlines()
        for cont in contents:
            cur_list = [int(c) for c in cont.split(",")]
            result_lists.append(cur_list)
    return result_lists


def construct_targets(path):
    result_lists = []
    with open(path, 'r') as f:
        contents = f.readlines()
        for cont in contents:
            result_lists.append(int(cont))
    return result_lists


def construct_results(path):
    result_lists = []
    with open(path, 'r') as f:
        contents = f.readlines()
        for cont in contents:
            result_lists.append(str(cont))
    return result_lists


def lists_target_dict():
    # list_dict: key = index, value = list
    # target_dict: key = index, value = targets
    target_dict = {}
    list_dict = {}
    DEST = "../data/"
    key_index = 0
    lists_target = []
    for p in os.listdir(DEST):
        res_lists = construct_lists(os.path.join(DEST, p))
        for item in res_lists:
            list_dict[key_index] = item
            # randomly create a targets
            num = random.randrange(1, len(item))
            target = sum(random.sample(item, num)) + random.randint(min(item), max(item))
            target_dict[key_index] = target
            lists_target.append((item, target))
            key_index += 1
    return list_dict, target_dict
