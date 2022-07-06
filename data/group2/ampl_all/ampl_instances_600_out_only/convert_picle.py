import os
import pickle


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
                solution.append(float(s_list[-1]))
                i += 1
            # print(solution)
            continue
        elif s_list[0][-1] == 's': # values:
            # print('values:', s_list)
            values = []
            i += 1
            while i < len(lines) and lines[i] != ';\n':
                s_list = lines[i].split(' ')
                values.append(float(s_list[-1]))
                i += 1
            # print(values)
        elif s_list[0][0] == 'c':
            calculated_sum = float(s_list[-1])
        elif s_list[0][0] == 't':
            target_sum = float(s_list[-1])
        elif s_list[0][0] == 's':
            set_len = int(s_list[-1])

        i += 1
    return run_time, calculated_sum, target_sum, set_len, solution, values


arr = os.listdir()
lp = []
ilp = []
for name in arr:
    if '_lp' in name:
        lp.append(name)
    elif '_ilp' in name:
        ilp.append(name)

# store ilp
ilp_pickle = []
for path in ilp:
    run_time, calculated_sum, target_sum, set_len, solution, values = process_out_single(path)
    one_res = [run_time, calculated_sum, target_sum, set_len, solution, values]
    ilp_pickle.append(one_res)

file = open('ilp_60.pickle', 'wb')
pickle.dump(ilp_pickle, file)
file.close()

# store lp
lp_pickle = []
for path in lp:
    run_time, calculated_sum, target_sum, set_len, solution, values = process_out_single(path)
    one_res = [run_time, calculated_sum, target_sum, set_len, solution, values]
    lp_pickle.append(one_res)

file = open('lp_60.pickle', 'wb')
pickle.dump(lp_pickle, file)
file.close()



file = open('lp_60.pickle', 'rb')
data = pickle.load(file)
# close the file
file.close()
# print(66666666666)
    # print(d)


print('converting to pickle. ')
