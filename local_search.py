from subset_algorithms import subset_sum_solver


def greedy_all(instance_paths):
    residue_all = []
    ratio_all = []
    results = []
    true_count = 0
    false_count = 0
    ns = []
    success_rate = []
    chose_set = []
    for item in instance_paths:
        # get 5 instances
        solver = subset_sum_solver(item)
        solver.read()
        # solve 5 instances with the same size
        res, residue, ratio, chose = solver.greedy_5_approximate()
        for i in range(len(res)):
            cur_res = res[i]
            if cur_res:
                true_count += 1
            else:
                false_count += 1
        results.append(res)
        residue_all.append(residue)
        ratio_all.append(ratio)
        ns.append(solver.n)
        success_rate.append(sum(res) / len(res))
        chose_set.append(chose)

    # print("results", results)
    # print("residue_all", residue_all)
    # print("ratio_all", ratio_all)
    # print("success_rate", success_rate)
    # print("chose_set", chose_set)
    return chose_set


if __name__ == "__main__":
    paths = ['data/group2/instances/n_42_b_30_count_5.npz']

