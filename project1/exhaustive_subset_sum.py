"""
The exhaustive algorithm will find all subset sum in input list. For each subset, check if the subset sum equals to
targets.
"""
from timeit import default_timer as timer
import func_timeout


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    from itertools import chain, combinations
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def exhaustive_search(l, k):
    for s in powerset(l):
        if sum(s) == k:
            return True
    return False


def run_function(f, my_argument, my_argument2, max_wait, default_value):
    try:
        return func_timeout.func_timeout(max_wait,
                                         f,
                                         args=[my_argument, my_argument2])
    except func_timeout.FunctionTimedOut:
        pass
    return default_value


def brute_force(arrays, t, ground_truth, instance_size, time_limit=1):
    num_instance = 0
    num_success = 0
    running_time_all = []
    for i in range(len(arrays)):
        cur_instance_size = len(arrays[i])
        if cur_instance_size != instance_size:
            continue

        num_instance += 1
        start = timer()

        # res = exhaustive_search(arrays[i], t[i])
        res = run_function(exhaustive_search, arrays[i], t[i], time_limit, 'time_exceed')
        if res == 'time_exceed':
            print(res)

        if ground_truth[i] == 'True\n':
            ground = True
        else:
            ground = False
        is_correct = ground == res
        if is_correct:
            num_success += 1

        end = timer()
        running_time = end - start
        running_time_all.append(running_time)
        # print('The running time is:', end - start)
    success_rate = num_success / num_instance
    running_time = sum(running_time_all) / len(running_time_all)

    return success_rate, running_time


def test_exhaustive(arrays, t, ground_truth, instance_size):
    num_instance = 0
    num_success = 0
    for i in range(len(arrays)):
        cur_instance_size = len(arrays[i])
        if cur_instance_size != instance_size:
            continue

        num_instance += 1
        start = timer()
        res = exhaustive_search(arrays[i], t[i])
        print('the result of the algorithm is:', res)
        print('ground truth:', ground_truth[i])

        if ground_truth[i] == 'True\n':
            ground = True
        else:
            ground = False

        is_correct = ground == res
        if is_correct:
            num_success += 1

        print('is_correct', is_correct)

        end = timer()
        running_time = end - start
        # print('The running time is:', end - start)
    success_rate = num_success / num_instance

    return success_rate, running_time
