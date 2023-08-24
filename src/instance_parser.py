import numpy as np


def get_CGLSP_instance_cost_matrix(instance_file_path):
    # get raw cost matrix from problem instance text file
    cost_matrix_raw = np.loadtxt(
        instance_file_path, dtype=int, delimiter=";")

    # insert an initial row and column for a dummy job to convert the problem into
    # an ASTP instead of a min Hamiltonian path problem

    # number of jobs = n
    n = cost_matrix_raw.shape[0]

    cost_matrix_augmented = np.zeros((n + 1, n + 1), dtype=int)
    cost_matrix_augmented[0, 0] = -1

    # insert cost matrix for real jobs into augmented cost matrix with dummy job
    cost_matrix_augmented[1:, 1:] = cost_matrix_raw

    # replace -1 in cost_matrix with "NA" as per Google_OR_TOOLS AP solver
    # specification

    cost_matrix_augmented = cost_matrix_augmented.astype(object)
    cost_matrix_augmented[cost_matrix_augmented == -1] = "NA"

    return cost_matrix_augmented
