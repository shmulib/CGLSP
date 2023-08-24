
from src.bnb_tree import BnB_Tree
from src.instance_parser import get_CGLSP_instance_cost_matrix
import sys
import time
from pathlib import Path
import numpy as np

# ensure cost matrices are printed to the console nicely by increasing the line
# width for printing numpy arrays
np.set_printoptions(precision=2, suppress=True, linewidth=100)


class CGLSP:
    def __init__(self, problem_instance, problem_type, update_frequency):

        if problem_type == "CGLSP":
            root_cost_matrix = get_CGLSP_instance_cost_matrix(
                problem_instance)

        else:
            root_cost_matrix = problem_instance

        instance_size = root_cost_matrix.shape[0]
        if problem_type == "CGLSP":
            self.num_coils = instance_size - 1
        else:
            self.num_coils = instance_size
        self.bnb_tree = BnB_Tree(root_cost_matrix, instance_size, update_frequency)
        self.min_cost = np.inf
        self.optimal_solution = []
        self.problem_type = problem_type

        if problem_type == "CGLSP":
            dashed_line = "-" * 80
            print(dashed_line)
            print(f"Solving CGLSP instance with {self.num_coils} coils \n")
            print("The cost matrix for this instance is: ")
            print(root_cost_matrix)

        elif problem_type == "TSPLIB":
            dashed_line = "-" * 80
            print(dashed_line)
            print(f"Solving TSPLIB ASTP instance with {self.num_coils} cities \n")
            print("The cost matrix for this instance is: \n")
            print(root_cost_matrix)

    def solve(self):

        start = time.time()
        self.min_cost, self.optimal_solution = self.bnb_tree.solve()
        end = time.time()
        self.solve_time = end - start

        self.optimal_sequence = [edge[0] for edge in self.optimal_solution]

        # 0 job is dummy node in graph, remove it in final solution to
        # obtain actual sequence of coils
        if self.problem_type == "CGLSP":
            self.optimal_sequence.remove(0)

        # min cost of -1 is returned when there are no feasible solutions to CGLSP
        # (Although for the Spansh CGLSP problem instances
        # the authors gaurantee that all instances have a solution)

        # In general though, a CGLSP instance may not have feasible solutions
        if self.min_cost == -1:
            raise InfeasibleCGLSPInstanceException(
                " There are no feasible solutions for this CGLSP instance"
            )

        self.log_result()

        return self.min_cost, self.optimal_sequence, self.solve_time

    def log_result(self):
        import csv

        # Create a subdirectory for CSV files (if it doesn't exist)
        subdirectory = "results"
        Path(subdirectory).mkdir(parents=True, exist_ok=True)

        if self.problem_type == "TSPLIB":
            file_name = "TSPLIB_ATSP_br17.csv"
            problem_instance = "br17"

        elif self.problem_type == "CGLSP":
            file_name = "CGLSP_17.csv"
            problem_instance = "cgl_17"

        # Path to the CSV file
        csv_file_path = Path(subdirectory) / file_name

        result = {"Problem Instance": problem_instance,
                  "# Coils to sequence": self.num_coils,
                  "Min Cost": self.min_cost,
                  "Optimal Sequence": self.optimal_sequence,
                  "Solve Time (s)": round(self.solve_time, 4),
                  "# Explored Subproblems": self.bnb_tree.explored_subproblems}

        # Write the result to the CSV file
        with csv_file_path.open(mode="w", newline="") as csv_file:
            fieldnames = [field for field in result]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()  # Write header row
            writer.writerow(result)


# custom expection class in case CGLSP instance is actually not solveable
class InfeasibleCGLSPInstanceException(Exception):
    pass


if __name__ == "__main__":

    def solve_instance(problem_instance, problem_type, update_frequency):

        CGLSP_instance = CGLSP(problem_instance, problem_type, update_frequency)
        min_cost, solution, solve_time = CGLSP_instance.solve()

        dashed_line = "-" * 80
        print(dashed_line)
        print("Solution: \n")
        print("Min cost: ", min_cost)
        print("Optimal coil sequence: ", solution)
        print("\nSolve Time = ",  format(solve_time, '.6f'), "seconds\n")

    class InvalidArgumentsError(Exception):
        pass

    if len(sys.argv) < 2:
        raise InvalidArgumentsError("You need to pass the type of problem instance you'd"
                                    " like to solve. Pass either 'TSPLIB' or 'CGLSP' ")

    elif len(sys.argv) > 3:
        message = ("Script takes at most 2 arguments. For the first argument, you "
                   "need to pass the type of problem instance you'd like to solve. "
                   "Pass either 'TSPLIB' or 'CGLSP'.\n"
                   "Optionally you can also control how often the progress "
                   "of the optimization process is reported by specifiying "
                   "an integer. A good default value is 500.")
        raise InvalidArgumentsError(message)

    else:
        problem_type = sys.argv[1]

        if len(sys.argv) == 2:
            update_frequency = 500

        elif len(sys.argv) == 3:
            try:
                int(sys.argv[2])
            except:
                raise InvalidArgumentsError("Update frequency argument must be an int.")
            update_frequency = int(sys.argv[2])

        if problem_type == "CGLSP":

            problem_instance_relative_path = \
                "problem_instances/CGLSP_instances/data/cgl_17.txt"
            problem_instance_absolute_path = \
                Path(problem_instance_relative_path).resolve()

            problem_instance = problem_instance_absolute_path

            solve_instance(problem_instance, problem_type, update_frequency)

        elif problem_type == "TSPLIB":

            from src.algorithm_verification.br17 import get_cost_matrix_br17_atsp
            cost_matrix = get_cost_matrix_br17_atsp()
            problem_instance = cost_matrix

            solve_instance(problem_instance, problem_type, update_frequency)

        else:
            raise InvalidArgumentsError("Pass only the type of problem instance you'd "
                                        "like to solve. Choose either 'TSPLIB' or 'CGLSP'")
