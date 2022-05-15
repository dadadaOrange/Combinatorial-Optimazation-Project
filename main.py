import argparse
from project1.generate_lists import save_lists_target_result, load_lists_target, save_results, generate_chart, \
    generate_lists
from project1.exhaustive_subset_sum import test_exhaustive, brute_force
import os
import numpy as np
import matplotlib.pyplot as plt


def main():
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
        "--data_path", type=str, default="data/group1", help="the path of instances"
    )
    args = parser.parse_args()
    # generate_data
    save_lists_target_result(args.instance_size, args.instance_number, args.range_min, args.range_max, args.data_path)
    # read the lists and target data from files
    instances, target, ground_truth = load_lists_target(args.data_path)

    # for report
    chart = generate_chart(instances, target, ground_truth)
    chart_path = os.path.join(args.data_path, "chart.csv")
    save_results(chart, chart_path)

    #test algorithm
    instance_sizes = [1, 3, 5]
    instance_sizes = [args.instance_size - i for i in range(args.instance_size - 1, -1, -2)]

    running_time_all = []
    success_rate_all = []
    for instance_size in instance_sizes:
        # success_rate, running_time = test_exhaustive(instances, target, ground_truth, instance_size)
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


if __name__ == "__main__":
    main()
    print("Code is done!")
