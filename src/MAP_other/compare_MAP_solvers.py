# from instance_parser import instance_to_cost_matrix
from src.instance_generation.random_CGLSP_instance_generator import get_random_CGLSP_instances
from src.MAP_other.MAP_brute_force_solver import *
from src.MAP_solver import google_or_AP_solver


# pass a list of ints, test_instances to get_random_CGLSP_instances to generate random problem instances
# where test_instances[i] is the num_jobs for test instance i
test_instances = list(range(3, 9))
num_test_instances = len(test_instances)
cost_matrices = get_random_CGLSP_instances(num_jobs=test_instances)

if num_test_instances == 1:
    cost_matrices = [cost_matrices]


print("\n--------------------------------------------START OF ALGORITHM COMPARISION---------------------------------------------------------------")

print(f"Comparing solutions from Google OR Solver and Brute Force solver for {num_test_instances} test instances \n")


failed_solves = 0
for i, cost_matrix in enumerate(cost_matrices):
    print("----------------------------------------------------------------------------------------------------------------------------------")

    print(
        f"Comparing solutions from Google OR Solver and Brute Force solver for test instance {i+1} / {num_test_instances} \n")

    best_sol_google, best_assignment_costs_google, min_cost_google = google_or_AP_solver(cost_matrix)

    print("----------------------------------------------------------------------------------------------------------------------------------")

    best_sol_bf, best_assignment_costs_bf, min_cost_bf = brute_force_AP_solver(cost_matrix)

    print("----------------------------------------------------------------------------------------------------------------------------------")

    print(
        f"Checking if Google OR solution and Brute Force solution are the same for test instance {i+1} / {num_test_instances} : \n")

    best_solution_assertion = {"condition": best_sol_google == best_sol_bf, "message": f"Google OR best solution {best_sol_google} is \
                                                not the same as Brute Force best solution {best_sol_bf}"}

    best_assignment_costs_assertion = {"condition": best_assignment_costs_google == best_assignment_costs_bf, "message":
                                       f"Google OR best solution assignment costs {best_assignment_costs_google}  is \
                                          not the same as Brute Force best solution assignment costs {best_assignment_costs_bf}"}

    min_cost_assertion = {"condition": min_cost_google == min_cost_bf, "message":
                          f"Google OR best solution min cost {min_cost_google}  is \
                                          not the same as Brute Force best solution min cost {min_cost_bf}"}

    assertions = [best_solution_assertion, best_assignment_costs_assertion, min_cost_assertion]

    failed_assertions = 0
    for assertion in assertions:
        condition = assertion["condition"]
        message = assertion["message"]
        try:
            assert condition, message
        except AssertionError as e:
            failed_assertions += 1
            print(f"Assertion Failed for test instance {i} : ",  e)

    if failed_assertions > 0:
        failed_solves += 1

    else:
        print(
            f"Google OR solution and Brute Force solution ARE THE SAMME for test instance {i+1} / {num_test_instances} \n")


if failed_solves == 0:

    print("----------------------------------------------------------------------------------------------------------------------------------")

    print("Congratulations, all test instances had the same solution for the Google OR solver and the Brute Force solver\n")

else:
    print(
        f"Unfortunately the brute force solver is giving the incorrect answer on {failed_solves} / {num_test_instances} instances\n")


print("--------------------------------------------END OF ALGORITHM COMPARISION---------------------------------------------------------------")
