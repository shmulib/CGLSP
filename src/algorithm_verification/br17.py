import numpy as np
import tsplib95


def get_cost_matrix_br17_atsp():

    from pathlib import Path

    relative_path = "problem_instances/TSPLIB_instances/br17.atsp"
    absolute_path = Path(relative_path).resolve()

    problem = tsplib95.load(absolute_path)

    broken_cost_matrix_list = problem.edge_weights

    cost_matrix_list = []
    i = 0
    while i < 34:
        if i % 2 == 0:
            row_first_half = problem.edge_weights[i]
            cost_matrix_list.append(row_first_half)
        else:
            row_second_half = problem.edge_weights[i]
            cost_matrix_list[-1] = cost_matrix_list[-1] + row_second_half

        i += 1
    cost_matrix = np.array(cost_matrix_list, dtype=object)

    cost_matrix[cost_matrix == 9999] = "NA"

    return cost_matrix


if __name__ == "__main__":
    cost_matrix = get_cost_matrix_br17_atsp()
    print(cost_matrix)
