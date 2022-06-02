import numpy as np
import os
import random
import csv
# from utils.utils import construct_lists, construct_targets, construct_results


def hello():
    print("generate list dir")


def generate_lists(max_list_size, lists_num, range_min, range_max):
    # instance_lists = np.zeros((lists_num, list_size))
    instance_lists = []
    sizes = [max_list_size - i for i in range(max_list_size - 1, -1, -2)]
    print(sizes)
    for i in range(lists_num):

        # cur_list_size = random.randint(1, max_list_size)
        for k in sizes:
            cur_list_size = k
            # generate a list with cur_list_size
            cur_list = []
            for j in range(cur_list_size):
                cur_list.append(random.randint(range_min, range_max))
            instance_lists.append(cur_list)
    return instance_lists


def save_lists_target_result(list_size, lists_num, range_min, range_max, path):
    # generate lists and save in ..lists.csv
    if not os.path.exists(path):
        print('making a new directory. ')
        os.makedirs(path)

    generated_lists = generate_lists(list_size, lists_num, range_min, range_max)

    with open(os.path.join(path, "lists.csv"), 'w') as f:
        write = csv.writer(f)
        for item in generated_lists:
            write.writerow(item)
    # generate targets and save in ...targets.csv
    generated_target = []
    generated_result = []
    for item in generated_lists:
        """
            90 % true targets = sum(random.sample(list(item), num))
            10 % false targets = 3.14
        """
        percent = random.uniform(0, 1)
        if percent <= 0.8:
            # True condition
            if len(item) == 1:
                target = item[0]
            else:
                num = random.randrange(1, len(item))
                # plus = random.randint(min(item), max(item))
                target = sum(random.sample(list(item), num))
        else:
            # False condition
            target = 1000000
        generated_target.append([target])
        cur_res = True if target != 1000000 else False
        generated_result.append([cur_res])
    with open(os.path.join(path, "targets.csv"), 'w') as f:
        write = csv.writer(f)
        for item in generated_target:
            write.writerow(item)

    with open(os.path.join(path, "results.csv"), 'w') as f:
        write = csv.writer(f)
        for item in generated_result:
            write.writerow(item)


def load_lists_target(data_path):
    lists = construct_lists(os.path.join(data_path, "lists.csv"))
    targets = construct_targets(os.path.join(data_path, "targets.csv"))
    results = construct_results(os.path.join(data_path, "results.csv"))
    # print("load", results)
    return lists, targets, results


def generate_chart(lists, targets, results):
    chart = []
    for i in range(len(targets)):
        chart.append([lists[i], targets[i], results[i]])
    return chart


def save_results(chart, data_path):
    Title = ['List', 'Target', 'Result']
    with open(data_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(Title)
        for item in chart:
            write.writerow(item)
