# CGLSP (Continuous Galvanizing Line Sequencing Problem)

The CGLSP is a sequencing problem that arises in the final stage production of steel coils. Steel coils can be required
to galvanised, i.e. coated with a zinc layer to protect them against air and mosture. The steel coils are coated in batches
where the coils in each batch are welded end to end to produce one continous strip of steel. This strip is then processed
through the galvanizing line with no downtime between the individual coils that compose the strip.

The sequence of the individual coils in the strip determines how much wastage of steel occurs as a result of the galvansing
line needing to be recalibrated between coils. When the line transitions from coating one coil to the next, wastage occurs
because the transition period of the line results in the beginning of the next coil being treated at suboptimal parameters.
This can produce a section of the coils which is inferior or unsaleable.

However, because of the relative settings required for different pairs of coils, the transition periods can be shortened
by sequencing the coils such that consecutive pairs of coils have less wastage.

Addtionally, because of phsyical differences in the individual coils, such as steel grade, some coils cannot be sequenced consecutively after other coils.

Moreover the order in which a pair of coils is consecutively sequenced can result in different amounts of wastage.

The complete choice of consecutive pairs forms a sequence, and the goal here to select a sequence to minimise aggregate wastage.

The solver implemented in this repo uses a graph theoretic formulation of the sequencing problem and finds the optimal sequence for a batch coils by using a branch and bound algorithm variant.

Details of the graph theoretic formulation of the problem, and the branch and bound algorithm used to solve it, can be found in the docs [here](docs/CGLSP_graph_formulation_and_branch_and_bound_solution.md)



## Table of Contents

- [Installation](#installation)
- [Problem Instances](#problem-instances)
- [Usage](#usage)
- [Graph Theory Formulation and Branch and Bound Solution](#graph-theory-formulation-and-branch-and-bound-solution)
- [Codebase Structure](#codebase-structure)
- [Results obtained used this solver](#results-obtained-used-this-solver)
- [Ideas for optimization algorithm improvement](#ideas-for-optimization-algorithm-improvement)



## Installation

To clone the repo and set up the required python virtual environment use the below commands. I use conda to manage virtual environemnts and have provided
an environment.yml file to create a conda virtual environment with the required dependencies. I also created a pip
compatible requirements.txt file in the dependencies directory, but an attempt to create a virtualenv virtual environment using pip failed due to pip being unable to find all required packages.

To clone the repo and setup the required conda virtual enviroment execute the following commands:

```
git clone https://github.com/shmulib/CGLSP.git
cd CGLSP
conda env create -f dependencies\environment.yml
```

## Problem Instances

This CGLSP sequencing problem orginates from research Spanish academics conducted for a Spanish steel manufacturing company.

I've provided the paper they wrote about their research on the CGLSP problem in the CGLSP_academic research directory of this repo. The paper is the file - Sequencing jobs with asymmetric costs and transition constraints.pdf

The authors also provide 30 real problem instances derived from actual batches of steel coils required to be sequenced at the steel manufacturer.

These 30 instances are provided in this repo in the problem_instances/CGLSP_instances/data directory.

Each problem instance file is labelled cgl_{num_coils}.txt where the num_coils is the number of steel coils required
to be galvanised in that batch.

The contents of the problem instance files are cost matrices for the batch where entry (i,j) is the cost of sequencing
coil j directly after coil i. All costs are non-negative except for pairs of coils that can't be sequence directly after
each other, where the cost is -1 to indicate infeasibility.

Further details of the problem instances are provided in the problem_instances/CGLSP_instaces/README.md file which was
provided by the Spanish academics who [shared the instances publicly](https://data.mendeley.com/datasets/v357z2ncbh/2).

You can also read about the problem instances in this paper written by the same academics, which is 
provided in this repo in CGLSP_academic_research/Problem_instances_dataset_of_a_real-world_sequencing_problem.pdf 

I have also provided another problem instance of the same graph theoretic optimization problem, i.e. Asymmetric Travelling
Salesman Problem. This instance is br17 from the ASTP problem instances in the TSPLIB95 database. The instance is located
in problem_instances/TSPLIB_instances/br17.atsp

The [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) database contains problem instances of a variety of different TSP problem variants including ATSP as well as optimal solutions for the instances where they are known.

The br17 instance has been provably solved to optimality. I have used this solver to solve the br17 instance to optimality as a means verifying correctness.

## Usage

The entry point to the solver is the CGLSP.py script in the src directory.

I've implemented a command line interface to run the solver using this script, for selected problem instances that I have successfully solved to optimality, i.e. cgl_17 and br17.

You can use the command line interface as follows to run the solver for these instances:

Ensure the current working directory is the root directory (CGLSP), then execute

```
python -m src.CGLSP <problem_type> <update_frequency>

```
Arguments: 

- 'problem_type': One of either 'CGLSP' or 'TSPLIB'. Selecting 'CGLSP' will run the solver for the
cgl_17 problem instance. Selecting 'TSPLIB' will run the solver for the TSPLIB ATSP br17 instance.
- 'update_frequency' (optional): This is an integer that controls the frequency of solver progress updates output to the console during the solve. Specifically, it is the number or branching operations between solver updates. The default value is 500, but this can be tuned to a more suitable value for a given problem instance by prematurely terminating the solver and trying again with a more desirable update frequency.

This command will run the solver for these specific instances of the chosen instance type. During the solve the solver will provide progress updates to the console at a frequency determined by the update_frequency argument. Once the instance has been solved to optimality final results will be logged and stored in the results directory in csv files labelled 'CGLSP_17' for the CGLSP instance and 'TSPLIB_ATSP_br17' for the TSPLIB instance.

This csv results file contains the following fields:

- Problem Instance,
- \# Coils to sequence,
- -Min (Optimal) Cost,
- Optimal Sequence,
- Solve Time (s),
- \# Explored Subproblems (The number of explored subproblems by the branch and bound algorithm)

The CGLSP.py script contains the CGLSP solver class which solves an instance based on being provided a cost matrix for that instance. It works with any correctly structured cost matrix, but the command line interface specifically passes the instances for either cgl_17 or br17. 

I have written an instance parser (in src/instance_parser.py) to convert the raw CGLSP problem instances provided by the Spanish academic researchers into cost matrices that can be used by the CGLSP solver.

By using the CGLSP.py script directly any of the CGLSP problem instances can be passed to the solver, but I haven't implemented the command line interface to provide this functionality yet, as the other instances cannot yet be solved
to optimality and my intention with the current command line interface was for it to be as clean/readable as possible.

I plan to update the command line interface to allow any instance to be selected, once I have implemented the solver improvements dicussed in the ["Ideas for optimization algorithm improvement"](#ideas-for-optimization-algorithm-improvement) section below.

## Graph Theory Formulation and Branch and Bound Solution

The CGLSP sequencing problem can be formulated as a graph theory optimization problem of finding a minimum cost Hamiltonian path on an incomplete asymmetric graph, or digraph.

The details of this graph theoretic formulation and the description of the branch and bound algorithm
this solver uses to solve it, will shortly be able to be found in the docs [here](docs/CGLSP_graph_formulation_and_branch_and_bound_solution.md)


## Codebase Structure

This repo implements a solver for the CGLSP sequencing problem. The structure of the codebase will shortly be described in the docs [here](docs/codebase_structure.md)

## Results obtained used this solver

This solver is used to find optimal solutions for CGLSP sequencing problem instances. The solver implements a variant of a branch and bound algorithm.

Utilizing the current implementation, without the addtional optimization improvements suggested in the improvements [section](#ideas-for-optimization-algorithm-improvement), the solver can solve the following instances to optimality

- The CGLSP instance with 17 coils \- cgl_17
    - The current solver, solves cgl_17 to optimality in about 0.30s, demonstrating that it can potentially solve instances very quickly.
- The TSPLIB (ASTP) instance  \- br17
    - This is not an CGLSP instance, but the graph theory formulation is the same as a CGLSP instance
    - The solver finds the known optimal solution, which is both, a proof of correctness, as well as evidence of the solver's ability to solve instances
      of this size for the CGLSP.
    - As the optimal cost for the br17 instance is known, we have determined that the optimal solution is found early on in the branch and bound algorithm, but the lower bounds determined for subproblems remain lower than the optimal solution for a relatively large number of subproblems that are branched to. Improvements in choice of branching variables and order of subproblems considered, explained in the possible solver improvements [section](#ideas-for-optimization-algorithm-improvement), may help reduce the size to which the branch and bound tree grows for this instance.

Instances attempted to be solved by the solver, but that don't currently terminate:

- The next largest CGLSP instance with 26 coils - CGLSP_26
    - The solver hasn't terminated when run for about 20 minutes, beacuse the branch and bound tree continues to grow. This occurs because the upper bounds obtained through finding optimal solutions of the Modified Assignment Problem (CGLSP relxation) for the subproblems, which are CGLSP feasible, are not lower than a large number of the lower bounds obtained for explored subproblems, and so these subproblems are branched on instead of pruned, resulting in a very inefficient branch and bound search. 
    - The improvements suggested [below](#ideas-for-optimization-algorithm-improvement) may bring this and other larger CGSLP instances into reach of the solver.


## Ideas for optimization algorithm improvement

Work still to be done






































