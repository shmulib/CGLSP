from instance_parser import instance_to_cost_matrix
import numpy as np
import time


def brute_force_AP_solver(cost_matrix):


    start_time = time.time() 

    print("Solving Assignment Problem using Brute Force \n")

    print("Cost Matrix: \n", cost_matrix, "\n")
    
    #generate all feasible solutions
    feasible_sols = generate_feasible_solutions(cost_matrix)


    #find the min cost feasbile solution
    if feasible_sols:

        print("Finding feasible solution with min cost: ")

        min_cost = np.inf
        best_sol = []
        best_assignment_costs = []
        for i, sol in enumerate(feasible_sols):
            cost, assignment_costs = feasible_sol_cost(sol, cost_matrix)
         #   print(f"Feasible Solution {i+1}/{len(feasible_sols)}: ", sol, "Assignment Costs: ", assignment_costs, "Total Cost: ", cost)
            if cost < min_cost:
                min_cost = cost
                best_sol = sol
                best_assignment_costs = assignment_costs

        end_time = time.time()
        elapsed_time = end_time - start_time

        print("\nBest Solution: ")


        print(f"\nTotal cost = {min_cost}\n")

        num_jobs = len(best_sol)
        for i in range(0, num_jobs):
            cur_job = i
            next_job = best_sol[i][1]
            print(
                f"Job {cur_job} precedes job {next_job}."
                + f"  Cost = {best_assignment_costs[i]}"
            )

        
        print("\nSolve Time = ",  format(elapsed_time, '.6f'), "seconds")
        
    else:
        print("No feasible solutions. Assignment is not possible.")

    return best_sol, best_assignment_costs, min_cost 



def generate_feasible_solutions(cost_matrix):

    print("Generating feasible solutions: ")

    cost_matrix = cost_matrix.tolist()

    n= len(cost_matrix)

    feasible_solutions = []
    
    partial_solutions  = [{"path":[(0,i)], "used_cols": {i}, "cur_row":0 }  for i in range(1,n)]
    while partial_solutions:
      #  print(partial_solutions)
        
        curr_path_object = partial_solutions.pop(0)
        curr_path = curr_path_object["path"]
        next_row = curr_path_object["cur_row"] + 1

        used_cols = curr_path_object["used_cols"]
        next_row_feasible_cols = {index for index, cost in enumerate(cost_matrix[next_row]) if cost!="NA" and index != next_row} - used_cols
        for col in next_row_feasible_cols:
            updated_path = curr_path.copy()
            updated_path.append((next_row,col))
            if len(updated_path) == n:
                feasible_solutions.append(updated_path)
               # print("feasible soloutions", feasible_solutions)
            else:
                new_used_cols = used_cols.union({col})
                cur_row = next_row
                updated_path_object = {"path": updated_path, "used_cols": new_used_cols, "cur_row": cur_row}
                partial_solutions.append(updated_path_object)
            
    print(f"There are {len(feasible_solutions)} feasible solutions \n")
    
    return feasible_solutions


def feasible_sol_cost(sol, cost_matrix):

    #cost matrix is a 2d numpy array, #TO DO - add Typing

    row_indices= [edge[0] for edge in sol ]

    col_indices = [edge[1] for edge in sol]

    assignment_costs = cost_matrix[row_indices, col_indices]

    cost = assignment_costs.sum()

    return cost, assignment_costs.tolist()


if __name__ == "__main__":

    #n=3

    cost_matrix = np.array([[i*j for i in range(4)] for j in range(4)] )
 
    
    # feasible_sols = generate_feasible_solutions(cost_matrix)

    # first_sol = feasible_sols[0]

    # print("Sol: ", first_sol)
    # cost = feasible_sol_cost(first_sol, cost_matrix)
    # print("Sol Cost": cost)

    best_sol, best_assignment_costs, min_cost = brute_force_AP_solver(cost_matrix)




    # instance_file_path = r"C:\Users\Shmuli\Desktop\Optimization\CGLSP\problem_instances\data\cgl_17.txt"
    # cost_matrix =  instance_to_cost_matrix(r"C:\Users\Shmuli\Desktop\Optimization\CGLSP\problem_instances\data\cgl_17.txt")
    # print(cost_matrix)


    # best_sol, min_cost = brute_force_AP_solver_cost_matrix(cost_matrix)

    # print("Best Sol: ", best_sol, "Min Cost: ", min_cost)





