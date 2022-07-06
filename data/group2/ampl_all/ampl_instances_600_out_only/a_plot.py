import pickle

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

def plot_results(sizes, times, title):
    x = sizes
    y = times
    plt.xlabel('Instance size')
    plt.title(title)
    # plt.ylabel('running time')
    plt.ylabel('Time')
    size = [i for i in range(2, 101, 4)]
    plt.xticks(size)
    plt.plot(x, y)
    plt.savefig('ampl_ILPlimit600.png')
    plt.show()



file = open('lp_60.pickle', 'rb')
data = pickle.load(file)
file.close()

# one_res = [run_time, calculated_sum, target_sum, set_len, solution, values]
dict_ins_size = defaultdict(list)
for one_res in data:
    dict_ins_size[one_res[3]].append(one_res)

size = [i for i in range(2, 101, 2)]
t = []
for i in size:
    cur = dict_ins_size[i]
    cur_sum = 0
    for one in cur:
        cur_sum += one[0]
    ave = cur_sum / 5
    t.append(ave)

title = 'LP Time Limit 60'
plot_results(size, t, title=title)
# print(size)
# print(t)




file = open('ilp_60.pickle', 'rb')
data = pickle.load(file)
file.close()

# one_res = [run_time, calculated_sum, target_sum, set_len, solution, values]
dict_ins_size = defaultdict(list)
for one_res in data:
    dict_ins_size[one_res[3]].append(one_res)

size = [i for i in range(2, 101, 2)]

t = []
for i in size:
    cur = dict_ins_size[i]
    cur_sum = 0
    for one in cur:
        cur_sum += one[0]
    ave = cur_sum / 5
    t.append(ave)


def save_results(path, *items):
    np.savez_compressed(path, items)

path = 'ILP_size_time_ratio.npz'
# ratio = size.copy()
ratio = [1 for _ in range(len(size))]

save_results(path, size, t, ratio)
path = 'LP_size_time_ratio.npz'
t = [0 for _ in range(len(size))]
save_results(path, size, t, ratio)


title = 'ILP Time Limit 600'
plot_results(size, t, title=title)
