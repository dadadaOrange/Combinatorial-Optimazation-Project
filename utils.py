from timeit import default_timer as timer
import func_timeout
import numpy as np
import matplotlib.pyplot as plt


def plot_results(sizes, times, y_label='time', y_range=False):
    x = sizes
    y = times
    plt.xlabel('Instance size')
    # plt.ylabel('running time')
    plt.ylabel(y_label)
    # plt.xticks(x)
    plt.xticks([i for i in range(2, 100, 4)])
    # plt.yticks([i * 0.2 for i in range(0, 6)])
    # plt.yticks([0.2, 0.6, 1.0, 1.2])
    if y_range:
        plt.ylim([0.975, 1.025])
    plt.plot(x, y)
    plt.savefig('plots/size50_limit60.png')
    plt.show()


def run_function(f, my_argument, my_argument2, max_wait, default_value):
    try:
        return func_timeout.func_timeout(max_wait,
                                         f,
                                         args=[my_argument, my_argument2])
    except func_timeout.FunctionTimedOut:
        pass
    return default_value


def timer_calculation(algo, arr, t, time_limit):
    start = timer()
    res = run_function(algo, arr, t, time_limit, 'time_exceed')
    if res == 'time_exceed':
        res = False
    end = timer()
    running_time = end - start
    return res, running_time


def all_results_timer(algo, arrays, targets, time_limit):
    if arrays is None or targets is None:
        raise ValueError('Please read data file.')
    results = []
    times = []
    for i in range(len(targets)):
        arr = arrays[i]
        t = targets[i]
        result, running_time = timer_calculation(algo, arr, t, time_limit)
        results.append(result)
        times.append(running_time)
    return results, times


def save_results(path, *items):
    np.savez_compressed(path, items)

