# Structure of the CCGLSP Solver Codebase

The CGLSP solver codebase's structure mirrors the structure of the branch and bound algorithm variant the solver uses to solve the CGLSP sequencing problem formulated as a [graph optimization problem](docs/CGLSP_graph_formulation_and_branch_and_bound_solution.md)

The codebase consists of the following scripts:

- CGLSP.py
- instance_parser.py
- bnb_tree.py
- node.py
- MAP_solver.py

The problem instances are located in subdirectories under the "problem_instances" directory:

- CGLSP instances: CGLSP_instances/data
- TSPLIB instances: TSPLIB_instances/


## CGLSP.py
