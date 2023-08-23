"""Solve assignment problem using linear assignment solver."""
import numpy as np

from ortools.graph.python import linear_sum_assignment

import time


def google_or_AP_solver(cost_matrix):
    """Linear Sum Assignment example."""

    start_time = time.time()
    assignment = linear_sum_assignment.SimpleLinearSumAssignment()

    rows = cols = cost_matrix.shape[0]

    cost = cost_matrix.tolist()

    for worker in range(0, rows):
        for task in range(0, cols):
            if cost[worker][task] != 'NA':
                assignment.add_arc_with_cost(worker, task, cost[worker][task])

    status = assignment.solve()

    end_time = time.time()
    elapsed_time = end_time - start_time

    best_sol = []
    best_assignment_costs = []

    if status == assignment.OPTIMAL:

        min_cost = assignment.optimal_cost()

        for i in range(0, assignment.num_nodes()):
            cur_job = i
            next_job = assignment.right_mate(i)
            best_sol.append((cur_job, next_job))
            assignment_cost = assignment.assignment_cost(i)
            best_assignment_costs.append(assignment_cost)

        return best_sol, min_cost, best_assignment_costs, "FOUND_OPTIMAL"
    elif status == assignment.INFEASIBLE:
        min_cost = -1
        return best_sol, min_cost, best_assignment_costs, "INFEASIBLE"
    elif status == assignment.POSSIBLE_OVERFLOW:
        min_cost = -1
        return best_sol, min_cost, best_assignment_costs, "POSSIBLE_OVERFLOW"


def google_or_AP_solver_verbose(cost_matrix):
    """Linear Sum Assignment example."""

    start_time = time.time()

    print("Solving Assignment Problem using Google OR Assignment Problem Solver \n")

    print("Cost Matrix: \n", cost_matrix, "\n")
    assignment = linear_sum_assignment.SimpleLinearSumAssignment()

    rows = cols = cost_matrix.shape[0]

    cost = cost_matrix.tolist()

    for worker in range(0, rows):
        for task in range(0, cols):
            if cost[worker][task] != 'NA':
                assignment.add_arc_with_cost(worker, task, cost[worker][task])

    status = assignment.solve()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Best Solution: ")

    best_sol = []
    best_assignment_costs = []

    if status == assignment.OPTIMAL:

        min_cost = assignment.optimal_cost()

        print(f"\nTotal cost = {min_cost}\n")
        for i in range(0, assignment.num_nodes()):
            cur_job = i
            next_job = assignment.right_mate(i)
            best_sol.append((cur_job, next_job))
            assignment_cost = assignment.assignment_cost(i)
            best_assignment_costs.append(assignment_cost)
            print(
                f"Job {cur_job} precedes job  {next_job}."
                + f"  Cost = {assignment_cost}"
            )
        print("\nSolve Time = ",  format(elapsed_time, '.6f'), "seconds\n")

        return best_sol, min_cost, best_assignment_costs, "FOUND_OPTIMAL"
    elif status == assignment.INFEASIBLE:
        print("No assignment is possible.")
        min_cost = -1
        return best_sol, min_cost, best_assignment_costs, "INFEASIBLE"
    elif status == assignment.POSSIBLE_OVERFLOW:
        print("Some input costs are too large and may cause an integer overflow.")
        min_cost = -1
        return best_sol, min_cost, best_assignment_costs, "POSSIBLE_OVERFLOW"


class PossibleOverflowException(Exception):
    pass


if __name__ == "__main__":
    pass
