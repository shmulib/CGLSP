# Structure of the CCGLSP Solver Codebase

The CGLSP solver codebase's structure mirrors the structure of the branch and bound algorithm variant the solver uses to solve the CGLSP sequencing problem formulated as a [graph optimization problem](docs/CGLSP_graph_formulation_and_branch_and_bound_solution.md)

The codebase consists of the following scripts:

- CGLSP.py
- instance_parser.py
- bnb_tree.py
- node.py
- MAP_solver.py

The problem instances are located in subdirectories under the "problem_instances" directory:

- CGLSP instances: CGLSP_instances/data/
- TSPLIB instances: TSPLIB_instances/


## CGLSP.py

The CGLSP.py script is the entry point to using the solver to solve a CGLSP problem instance. This script contains the CGLSP class which orchestrates the solving of a CGLSP (or equivlent theoretical problem) instance. 

To instatiate the CGLSP class, one needs to pass a problem instance. Currently the CGLSP problem instances are pass as file paths to CGLSP solver class, which then uses the instance_parser.py script to parse the CGLSP problem instance file, returning the cost matrix for that problem instance.

The CGLSP instance class then creates an instance of the BnB_Tree class as an instance variable which can then be used to execute the branch and bound which is initiated by calling the CGLSP.solve method.

When the branch and bound is finished solving it returns the minimum cost and optimal solution (optimal Hamiltonian cycle on the augmented graph).

The CGLSP solve method will then convert the optimal Hamiltonian cycle into an optimal Hamiltonian path, i.e. the valid sequence of coils with minimum aggregate wastage.

It will then log results to a csv file in the "results" directory.



## bnb_tree.py

The bnb_tree.py script contains the BnB_Tree class, which is primary orchestrator of the branch and bound solve. The BnB_Tree class implements the branch and bound tree.

It is instantiated with a root node containing the full optimization problem to be solved. The root node is an instance of the Node class which is defined the node.py script.

When the BnB_Tree.solve method is called for a given BnB_Tree instance (by the CGLSP class object it belongs to), the branch and bound search is executed.

Initially the root node is explored, and an attempt to solve the full CGLSP optimization problem without exploring any subproblems is made. If the CGLSP problem instance can't be optimized using the root node alone, then the root node is branched using the BnB_Tree.branch method. The branching creates child subproblems, themselves instances of the Node class.

These subproblems are then explored. Where they can be pruned (/not branched on) from the branch and bound tree, because they can't contain the optimal solution of the CGLSP problem (/or because they can't contain a better solution to the CGLSP problem, then one obtained so far), they are. Otherwise, they are added to a collection of unpruned nodes, that need to be branched on, which is implemented as priority queue which is instance variable of the BnB_Tree object.

After all the subproblems of the currently being branched on problems have been explored, the next unpruned suproblem that has been created (with the lowest obtained lower bound on its optimal solution) is branched on next.

This process is continued until all subproblems created are either pruned or don't required branching.

At this point the BnB_Tree.solve method returns the optimal solution to the CGLSP problem instance.


# node.py

The node.py script contains the Node class which implements the subproblems that are explored in the branch and bound tree.

The Node instances contain all the information about their subprolem, included the edges of the CGSLP graph fixed in the subproblem, the suproblem cost matrix, and the best known lower bound obtained for the subproblem.

The Node instances implement the methods for lower bounding the subproblems as well as obtaining (better) upper bounds for the full CGLSP problem.

For lower bounding (the subproblem), the Node instances implement both cost reduction lower bound and lower bounding via solving a relaxtion of the CGLSP optimization problem 

The relaxation lower bound, as described [here](docs/CGLSP_graph_formulation_and_branch_and_bound_solution.md) in the "Branch and Bound" solution section, involves solving the Modified Assignment Problem for this subproblem.

Solving the Modified Assignment Problem for the subproblem both produces a lower bound (potentially tighter than by cost reduction lower bounding), as well as generates upper bounds for the CGLSP full optimization problem, where the MAP optimal solution for the subproblem is CGLSP feasible.

The BnB_Tree object will call the MAP_sol_CGSLP_feasible method for a subproblem Node to determine if the MAP optimal solution for that subproblem is CGLSP feasible, and if it is, it will update the best upper bound known for the CGLSP problem, where the upper bound is an improvement (which in the logic of the code, it always is).

After the subproblems have been lower bounded, the BnB_Tree will compare the best found lower bound to the best upper bound found so far, to determine whether the subproblem can be pruned, not branched on, or will require branching, and therefore needs to be added to the queue of unpruned nodes.





