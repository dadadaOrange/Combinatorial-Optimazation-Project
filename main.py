import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from data_generation import subset_sum_data
from subset_algorithms import subset_sum_solver
from utils import all_results_timer, save_results, plot_results


def project1():
    # Pass the argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--instance_size", type=int, default=3, help="Size of instance"
    )
    parser.add_argument(
        "--instance_number", type=int, default=5, help="Number of instance"
    )
    parser.add_argument(
        "--range_min", type=int, default=0, help="minimum value of the instance"
    )
    parser.add_argument(
        "--range_max", type=int, default=10, help="maximum value of the instance"
    )
    parser.add_argument(
        "--data_path", type=str, default="data/group3", help="the path of instances"
    )
    args = parser.parse_args()
    # generate_data
    save_lists_target_result(args.instance_size, args.instance_number, args.range_min, args.range_max, args.data_path)
    # read the lists and targets data from files
    instances, target, ground_truth = load_lists_target(args.data_path)

    # for report
    chart = generate_chart(instances, target, ground_truth)
    chart_path = os.path.join(args.data_path, "chart.csv")
    save_results(chart, chart_path)

    # test algorithm
    instance_sizes = [1, 3, 5]
    instance_sizes = [args.instance_size - i for i in range(args.instance_size - 1, -1, -2)]

    running_time_all = []
    success_rate_all = []
    for instance_size in instance_sizes:
        # success_rate, running_time = test_exhaustive(instances, targets, ground_truth, instance_size)
        print('doing', instance_size)
        success_rate, running_time = brute_force(instances, target, ground_truth, instance_size, time_limit=800)
        running_time_all.append(running_time)
        success_rate_all.append(success_rate)

    print(running_time_all, success_rate_all)

    file_name = args.data_path + '/data_pot.npz'
    np.savez_compressed(file_name, instance_sizes, running_time_all, success_rate_all)

    # read files
    with np.load(file_name) as f:
        instance_size = f["arr_" + str(0)]
        running_time = f["arr_" + str(1)]
        success_rate = f["arr_" + str(2)]

    # plot
    plot = True
    if plot:
        x = instance_size
        y = running_time
        plt.xlabel('instance size')
        plt.ylabel('running time')
        plt.xticks(x)
        plt.plot(x, y)
        plt.show()


def generate_instances(min_size, max_size, stride, path, b, count):
    files_path = []
    for n in range(min_size, max_size + 1, stride):
        file_name = path + '/instances/n_' + str(n) + '_b_' + str(b) + '_count_' + str(count) + '.npz'
        files_path.append(file_name)
        data = subset_sum_data(file_name)
        data.generate_density_data(n, b, count)
    return files_path


def run_exhaustive(files_path, save_path, time_limit):
    res_paths = []
    for f in files_path:
        solver = subset_sum_solver(f)
        solver.read()
        n = len(solver.arrays[0])

        results, times = all_results_timer(solver.exhaustive_search, solver.arrays, solver.targets, time_limit)
        # split f
        basename = os.path.basename(f)

        res_dir = save_path + '/exhaustive'
        if not os.path.exists(res_dir):
            print('making folder. ')
            os.makedirs(res_dir)
        result_path = res_dir + '/res_' + basename
        res_paths.append(result_path)
        ns = [n] * len(results)
        save_results(result_path, results, times, ns)
    return res_paths


def process_result(files_paths):
    """
    :param files_path:
    :return:
        1. list of sizes
        2. list of average running times
    """
    sizes = []
    ave_times = []
    for path in files_paths:
        # print(path)

        with np.load(path) as f:
            results = f["arr_" + str(0)][0]
            times = f["arr_" + str(0)][1]
            n = f["arr_" + str(0)][2][0]
            average_time = sum(times) / len(times)
            ave_times.append(average_time)
            sizes.append(n)
    success_rate = sum(results) / len(results)
    print("success rate :", success_rate)
    return sizes, ave_times

def greedy_all(instance_paths):
    # Greedy
    results = []
    true_count = 0
    false_count = 0
    index = 0
    ns = []
    success_rate = []
    for item in instance_paths:
        solver = subset_sum_solver(item)
        solver.read()
        result = solver.greedy()
        for item in result:
            if item:
                true_count += 1
            else:
                false_count += 1
        results.append(result)
        ns.append(solver.n)
        success_rate.append(sum(result) / len(result))

    print(ns)
    print(success_rate)
    print("true", true_count)
    print("false", false_count)

    ## plot
    plot_results(ns[:100], success_rate[:100])

if __name__ == "__main__":
    # Pass the argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--min_size", type=int, default=2, help="Min Size of instance"
    )
    parser.add_argument(
        "--max_size", type=int, default=10, help="Max Size of instance"
    )
    parser.add_argument(
        "--stride", type=int, default=5, help="Stride of the size"
    )
    parser.add_argument(
        "--path", type=str, default="data/group2", help="the path of instances"
    )
    parser.add_argument(
        "--bit", type=int, default=2, help="bit length"
    )
    parser.add_argument(
        "--count", type=int, default=10, help="the count of instance created for each size"
    )
    parser.add_argument(
        "--time_limit", type=int, default=60, help="the count of instance created for each size"
    )

    args = parser.parse_args()
    # instance_paths = generate_instances(args.min_size, args.max_size, args.stride, args.path, args.bit, args.count)
    # print(instance_paths)
    instance_paths = ['data/group2/instances/n_2_b_30_count_5.npz', 'data/group2/instances/n_4_b_30_count_5.npz',
                      'data/group2/instances/n_6_b_30_count_5.npz', 'data/group2/instances/n_8_b_30_count_5.npz',
                      'data/group2/instances/n_10_b_30_count_5.npz', 'data/group2/instances/n_12_b_30_count_5.npz',
                      'data/group2/instances/n_14_b_30_count_5.npz', 'data/group2/instances/n_16_b_30_count_5.npz',
                      'data/group2/instances/n_18_b_30_count_5.npz', 'data/group2/instances/n_20_b_30_count_5.npz',
                      'data/group2/instances/n_22_b_30_count_5.npz', 'data/group2/instances/n_24_b_30_count_5.npz',
                      'data/group2/instances/n_26_b_30_count_5.npz', 'data/group2/instances/n_28_b_30_count_5.npz',
                      'data/group2/instances/n_30_b_30_count_5.npz', 'data/group2/instances/n_32_b_30_count_5.npz',
                      'data/group2/instances/n_34_b_30_count_5.npz', 'data/group2/instances/n_36_b_30_count_5.npz',
                      'data/group2/instances/n_38_b_30_count_5.npz', 'data/group2/instances/n_40_b_30_count_5.npz',
                      'data/group2/instances/n_42_b_30_count_5.npz', 'data/group2/instances/n_44_b_30_count_5.npz',
                      'data/group2/instances/n_46_b_30_count_5.npz', 'data/group2/instances/n_48_b_30_count_5.npz',
                      'data/group2/instances/n_50_b_30_count_5.npz', 'data/group2/instances/n_52_b_30_count_5.npz',
                      'data/group2/instances/n_54_b_30_count_5.npz', 'data/group2/instances/n_56_b_30_count_5.npz',
                      'data/group2/instances/n_58_b_30_count_5.npz', 'data/group2/instances/n_60_b_30_count_5.npz',
                      'data/group2/instances/n_62_b_30_count_5.npz', 'data/group2/instances/n_64_b_30_count_5.npz',
                      'data/group2/instances/n_66_b_30_count_5.npz', 'data/group2/instances/n_68_b_30_count_5.npz',
                      'data/group2/instances/n_70_b_30_count_5.npz', 'data/group2/instances/n_72_b_30_count_5.npz',
                      'data/group2/instances/n_74_b_30_count_5.npz', 'data/group2/instances/n_76_b_30_count_5.npz',
                      'data/group2/instances/n_78_b_30_count_5.npz', 'data/group2/instances/n_80_b_30_count_5.npz',
                      'data/group2/instances/n_82_b_30_count_5.npz', 'data/group2/instances/n_84_b_30_count_5.npz',
                      'data/group2/instances/n_86_b_30_count_5.npz', 'data/group2/instances/n_88_b_30_count_5.npz',
                      'data/group2/instances/n_90_b_30_count_5.npz', 'data/group2/instances/n_92_b_30_count_5.npz',
                      'data/group2/instances/n_94_b_30_count_5.npz', 'data/group2/instances/n_96_b_30_count_5.npz',
                      'data/group2/instances/n_98_b_30_count_5.npz', 'data/group2/instances/n_100_b_30_count_5.npz']

    # np.savez_compressed(args.path, instance_paths)
    # read all path in a certain directory
    # Run exhaustive algorithm and get the result path
    # instance_paths = os.listdir(args.path + "/instances/")
    # instance_paths.sort()
    # print("instance_paths", instance_paths)
    # new_list = [args.path + "/instances/" + x for x in instance_paths]
    # print("new_list", new_list)
####################################################################################
    # res_paths = run_exhaustive(instance_paths, args.path, args.time_limit)
    # print("result_path", res_paths)
    # sizes, times = process_result(res_paths)
    # plot_results(sizes, times)
####################################################################################

    greedy_all(instance_paths)
    print("Code is done!")
