import argparse
import numpy as np
import os
import random
from exhaustive_subset_sum import test_exhaustive


def generate_save_lists(list_size, lists_num, range_min, range_max, path):
    instance_lists = np.zeros((lists_num, list_size))
    for i in range(lists_num):
        instance_lists[i, :] = np.random.randint(range_min, range_max, list_size)
    # Save the instances to .txt file in path
    np.savetxt(path, instance_lists, delimiter=',', fmt='%d')


def construct_lists(path):
    result_lists = []
    with open(path, 'r') as f:
        contents = f.readlines()
        for cont in contents:
            cur_list = [int(c) for c in cont.split(",")]
            result_lists.append(cur_list)
    return result_lists


def setup_target():
    # list_dict: key = index, value = list
    # target_dict: key = index, value = target
    target_dict = {}
    list_dict = {}
    DEST = "../data/"
    key_index = 0
    for p in os.listdir(DEST):
        res_lists = construct_lists(os.path.join(DEST, p))
        for item in res_lists:
            list_dict[key_index] = item
            # randomly create a target
            num = random.randrange(1, len(item))
            possible_target = sum(random.sample(item, num))
            target_dict[key_index] = possible_target + random.randint(min(item), max(item))
            key_index += 1
    return list_dict, target_dict


def main():
    # Pass the argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--instance_size", type=int, default=10, help="Size of instance"
    )
    parser.add_argument(
        "--instance_number", type=int, default=10, help="Number of instance"
    )
    parser.add_argument(
        "--range_min", type=int, default=0, help="minimum value of the instance"
    )
    parser.add_argument(
        "--range_max", type=int, default=10, help="maximum value of the instance"
    )
    parser.add_argument(
        "--data_path", type=str, default="../data/group_1.txt", help="the path of instances"
    )
    args = parser.parse_args()
    # generate_data
    generate_save_lists(10, 5, 0, 100, args.data_path)
    instances, target = setup_target()
    # run subset sum algorithms
    running_time = test_exhaustive(instances, target)
    print('the exhaustive algorithm running time:', running_time)


if __name__ == "__main__":
    main()
    print("Code is done!")
