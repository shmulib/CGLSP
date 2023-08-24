import numpy as np
import math


def get_random_CGLSP_instances(num_jobs, cost_lower_bound=1, cost_upper_bound=100, forbidden_job_pairs=True):

    if type(num_jobs) == int:
        instance_sizes = [num_jobs]

    else:
        instance_sizes = num_jobs

    cost_matrices_augmented = []

    for instance_size in instance_sizes:

        cost_matrix_augmented = np.zeros((instance_size + 1, instance_size + 1), dtype=int)

        cost_matrix = np.random.randint(cost_lower_bound, cost_upper_bound + 1, size=(instance_size, instance_size))

        # if forbidden pairs of consecutive jobs have been requested
        if forbidden_job_pairs != False:
            # if the number of forbidden jobs pairs has not been specified
            if forbidden_job_pairs == True:
                # chose a random int between 1 and a quarter of the edges in the complete graph
                # to delete
                K = math.floor(instance_size*(instance_size-1)/4)
                forbidden_job_pairs = np.random.randint(1, K+1)

            edges_to_delete = set()
            while len(edges_to_delete) < forbidden_job_pairs:
                row_index = np.random.choice(instance_size)
                col_index_choices = list(range(instance_size))
                col_index_choices.remove(row_index)
                col_index = np.random.choice(col_index_choices)
                edge = (row_index, col_index)
                if edge not in edges_to_delete:
                    edges_to_delete.add(edge)

            row_indices = [edge[0] for edge in edges_to_delete]
            col_indices = [edge[1] for edge in edges_to_delete]

            cost_matrix[row_indices, col_indices] = -1

        cost_matrix_augmented[1:, 1:,] = cost_matrix

        np.fill_diagonal(cost_matrix_augmented, -1)

        cost_matrix_augmented = cost_matrix_augmented.astype(object)
        cost_matrix_augmented[cost_matrix_augmented == -1] = "NA"

        cost_matrices_augmented.append(cost_matrix_augmented)

    if len(cost_matrices_augmented) == 1:

        return cost_matrices_augmented[0]

    else:
        return cost_matrices_augmented


if __name__ == "__main__":

    num_jobs = [3, 4, 5, 5]
    cost_matrices = get_random_CGLSP_instances(num_jobs=num_jobs)
    if type(cost_matrices) != list:
        cost_matrix = cost_matrices
        print(cost_matrix)
    else:
        for i, cost_matrix in enumerate(cost_matrices):
            print(f"Instance {i} :", cost_matrix)
