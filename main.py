import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from data_generation import subset_sum_data
from subset_algorithms import subset_sum_solver
from utils import all_results_timer, save_results, plot_results
import pickle
from timeit import default_timer as timer
import random

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
    ratios = []
    for item in instance_paths:
        solver = subset_sum_solver(item)
        solver.read()
        result, ratio = solver.greedy()
        for item in result:
            if item:
                true_count += 1
            else:
                false_count += 1
        results.append(result)
        ns.append(solver.n)
        ratios.append(sum(ratio) / len(ratio))

        success_rate.append(sum(result) / len(result))

    print(ns)
    print(ratios)
    print(success_rate)
    print("true", true_count)
    print("false", false_count)

    ## plot
    plot_results(ns[:100], success_rate[:100])
    plot_results(ns[:100], ratios[:100])


def generate_dat_run_ampl(instance_path, target_path):
    with np.load(instance_path) as f:
        arrays = f["arr_" + str(0)]
        targets = f["arr_" + str(1)]
        n = len(arrays[0])
    print('loading. ')
    # print('arrays', arrays)   # five arrays
    print('target:', targets)
    print('n', n)
    # print(instance_path)
    base = os.path.basename(instance_path)
    # print('base', base)
    base = base.split('.')
    # print('split base', base)
    base = base[0]


    if not os.path.exists(target_path):
        print('making folder. ')
        os.makedirs(target_path)
    for i in range(5):
        cur_arr = arrays[i]
        cur_target = targets[i]

        ######### generate .dat
        data_file_name = target_path + base + '_' + str(i) + '.dat'
        fhandle = open(data_file_name, 'w')
        # fhandle.write('abc, d '+ ';\n')
        fhandle.write('param set_len = ' + str(n) + ';\n')
        fhandle.write('param target_sum = ' + str(cur_target) + ';\n')
        fhandle.write('param values := ')

        for index, num in enumerate(cur_arr):
            fhandle.write('[%s] %s ' % (index+1, num))

        fhandle.write(';\n')
        fhandle.close()
        ######### generate .run  for lp
        run_file_name = target_path + base + '_' + str(i) + '_lp' + '.run'
        out_file_name = base + '_' + str(i) + '_lp' + '.out'

        fhandle = open(run_file_name, 'w')
        fhandle.write('model lp.mod;\n')

        data_file_name_base = os.path.basename(data_file_name)
        fhandle.write('data %s;\n' % data_file_name_base)
        fhandle.write('\n')

        fhandle.write('option solver cplex;\n')
        fhandle.write("option cplex_options 'timelimit=60';\n")
        fhandle.write("option cplex_options 'integrality=3e-07';\n")
        fhandle.write('solve;\n')
        fhandle.write('\n')

        fhandle.write('display _solve_elapsed_time > %s;\n' % out_file_name)
        fhandle.write('display calculated_sum > %s;\n' % out_file_name)
        fhandle.write('display target_sum > %s;\n' % out_file_name)
        fhandle.write('display set_len > %s;\n' % out_file_name)
        fhandle.write('display x > %s;\n' % out_file_name)
        fhandle.write('display values > %s;\n' % out_file_name)
        fhandle.write('\n')
        fhandle.close()

        ######### generate .run
        run_file_name = target_path + base + '_' + str(i) + '_ilp'+ '.run'
        out_file_name = base + '_' + str(i) + '_ilp' + '.out'

        fhandle = open(run_file_name, 'w')
        fhandle.write('model ilp.mod;\n')

        data_file_name_base = os.path.basename(data_file_name)
        fhandle.write('data %s;\n' % data_file_name_base)
        fhandle.write('\n')

        fhandle.write('option solver cplex;\n')
        fhandle.write("option cplex_options 'timelimit=60';\n")
        fhandle.write("option cplex_options 'integrality=3e-07';\n")
        fhandle.write('solve;\n')
        fhandle.write('\n')

        fhandle.write('display _solve_elapsed_time > %s;\n' % out_file_name)
        fhandle.write('display calculated_sum > %s;\n' % out_file_name)
        fhandle.write('display target_sum > %s;\n' % out_file_name)
        fhandle.write('display set_len > %s;\n' % out_file_name)
        fhandle.write('display x > %s;\n' % out_file_name)
        fhandle.write('display values > %s;\n' % out_file_name)
        fhandle.write('\n')
        fhandle.close()




    # with open(data_file_name) as f:
    #     lines = f.readlines()
    # print(lines)

def process_out_single(path):
    # print('processing file:', path)
    run_time = 0
    with open(path) as f:
        lines = f.readlines()
    # print(lines)
    # print(len(lines))
    i = 0
    while i < len(lines):
    # for line in lines:
        line = lines[i]
        # print(line)
        s_list = line.split(' ')
        # print(s_list)
        if s_list[0][-1] == 'e':  # runtime: '_solve_elapsed_time'
            # print('runtime:', s_list)
            run_time = float(s_list[-1])
        elif s_list[0][-1] == 'x': # solution: x [*] :=
            # print('solution:', s_list)
            solution = []
            i += 1
            while i < len(lines) and lines[i] != ';\n':
                s_list = lines[i].split(' ')
                solution.append(int(s_list[2]))
                i += 1
            # print(solution)
            continue
        elif s_list[0][-1] == 's': # values:
            # print('values:', s_list)
            values = []
            i += 1
            while i < len(lines) and lines[i] != ';\n':
                s_list = lines[i].split(' ')
                values.append(int(s_list[-1]))
                i += 1
            # print(values)
        elif s_list[0][0] == 'c':
            calculated_sum = int(s_list[-1])
        elif s_list[0][0] == 't':
            target_sum = int(s_list[-1])
        elif s_list[0][0] == 's':
            set_len = int(s_list[-1])

        i += 1
    return run_time, calculated_sum, target_sum, set_len, solution, values

def local_search(paths, itr_max=1000000, time_limit=60, tolerance=500, strategy='steepest', ini='random'):
    print('running.....', strategy, 'initial solution:', ini)
    run_times = []
    ns = []
    ratios = []
    itrs = []

    for path in paths:
        print(path)
        # if strategy == 'steepest':
        solver = subset_sum_solver(path, itr_max=itr_max, time_limit=time_limit, tolerance=tolerance)
        # elif strategy == 'anneal':

        solver.read()
        greedy_ini = solver.greedy_5_approximate()

        # result = solver.greedy()
        ratio_total = 0
        time_total = 0
        itr_count_total = 0
        for i, (single_instance, single_target) in enumerate(zip(solver.arrays, solver.targets)):
            # print('processing single input. ', i)
            # print(single_instance, single_target)
            if ini =='random':
                random_int = random.randrange(2, solver.n + 1)
                initial_solution = random.sample(list(single_instance), random_int)
            elif ini == 'greedy':
                initial_solution = greedy_ini[i]
            else:
                raise ValueError
            # print(ini)
            if strategy == 'steepest':
                residue, resulted_subset, running_time, itr_count = solver.steepest(single_instance, single_target, initial_solution)
            elif strategy == 'anneal':
                residue, resulted_subset, running_time, itr_count = solver.simulated_annealing(single_instance, single_target, initial_solution)
            else:
                raise ValueError
            # print(residue, resulted_subset, running_time)

            ratio = (single_target - residue) / single_target
            ratio_total += ratio
            time_total += running_time
            itr_count_total += itr_count
        ave_ratio = ratio_total / len(solver.targets)
        ave_time = time_total / len(solver.targets)
        ave_itr = itr_count_total / len(solver.targets)
        ratios.append(ave_ratio)
        run_times.append(ave_time)
        ns.append(solver.n)
        itrs.append(ave_itr)
        # print(ratios)
        # print(run_times)
        # print(ns)
    # save_results()
    return ratios, run_times, ns, itrs


def anneal_all(paths, itr_max=1000000, time_limit=60, tolerance=500):
    print('simulated_annealing.....')
    run_times = []
    ns = []
    ratios = []

    for path in paths:
        print(path)
        solver = subset_sum_solver(path, itr_max=itr_max, time_limit=time_limit, tolerance=tolerance)
        solver.read()
        # result = solver.greedy()
        ratio_total = 0
        time_total = 0
        for single_instance, single_target in zip(solver.arrays, solver.targets):
            # print('processing single input. ')
            # print(single_instance, single_target)
            random_int = random.randrange(2, solver.n + 1)
            # fixme ini using different strategy
            ini = random.sample(list(single_instance), random_int)
            # print(ini)
            residue, resulted_subset, running_time = solver.simulated_annealing(single_instance, single_target, ini)
            # print(residue, resulted_subset, running_time)

            ratio = (single_target - residue) / single_target
            ratio_total += ratio
            time_total += running_time
        ave_ratio = ratio_total / len(solver.targets)
        ave_time = time_total / len(solver.targets)
        ratios.append(ave_ratio)
        run_times.append(ave_time)
        ns.append(solver.n)
        # print(ratios)
        # print(run_times)
        # print(ns)
    # save_results()
    return ratios, run_times, ns

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
        "--experiment", type=str, default="steepest", help="the path of instances"
    )

    parser.add_argument(
        "--ini", type=str, default="random", help="the path of instances"
    )

    parser.add_argument(
        "--bit", type=int, default=2, help="bit length"
    )


    parser.add_argument(
        "--tolerance", type=int, default=50000, help="bit length"
    )

    parser.add_argument(
        "--max_itr", type=int, default=500000000, help="bit length"
    )

    parser.add_argument(
        "--time_limit", type=int, default=60, help="bit length"
    )

    parser.add_argument(
        "--count", type=int, default=10, help="the count of instance created for each size"
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


################# steepest   ####################################################
    if args.experiment == 'steepest':
        # ratios, run_times, ns = local_search(instance_paths, strategy=args.experiment,
        #                                      ini=args.ini, tolerance=args.tolerance)
        ratios, run_times, ns, itrs = local_search(instance_paths, itr_max=args.max_itr, time_limit=args.time_limit, ini=args.ini, strategy=args.experiment, tolerance=args.tolerance)

        save_path = args.experiment + '_' + args.ini + '_tolerance_' + str(args.tolerance) + '_time_limit_' + str(args.time_limit) + '.npz'
        save_results(save_path, ratios, run_times, ns, itrs)
        plot_results(ns, run_times, 'time')
        plot_results(ns, ratios, 'ratio', y_range=True)
        # anneal_all(instance_paths)
    elif args.experiment == 'anneal':
        ratios, run_times, ns, itrs = local_search(instance_paths, itr_max=args.max_itr, time_limit=args.time_limit, ini=args.ini, strategy=args.experiment, tolerance=args.tolerance)

        # ratios, run_times, ns = local_search(instance_paths, itr_max=args.max_itr, time_limit=args.time_limit, ini=args.ini, strategy=args.experiment, tolerance=args.tolerance)
        # save_path = 'tt.npz' #
        save_path = args.experiment + '_' + args.ini + '_tolerance_' + str(args.tolerance) + '_time_limit_' + str(args.time_limit) + '.npz'

        # save_path = args.experiment + '_' + args.ini + '_tolerance_' + str(args.tolerance) + '.npz'
        save_results(save_path, ratios, run_times, ns, itrs)
        plot_results(ns, run_times, 'time')
        plot_results(ns, itrs, 'number of iteration')
        plot_results(ns, ratios, 'ratio', y_range=True)
        # anneal_all(instance_paths)
    elif args.experiment == 'test':
        print(args.experiment)
        instance_paths = ['data/group2/instances/n_2_b_30_count_5.npz', 'data/group2/instances/n_4_b_30_count_5.npz',  'data/group2/instances/n_6_b_30_count_5.npz']
        test_path = instance_paths[2]
        solver = subset_sum_solver(test_path)
        solver.read()
        print(solver.arrays[1])
        ini = [448655659, 927737657]
        instance = solver.arrays[1]
        t = solver.targets[1]
        result = solver.steepest(instance, t, ini)
        print(result)

    print("Code is done!")
