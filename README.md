# CGLSP (Continuous Galvanizing Line Sequencing Problem)

The CGLSP is a sequencing problem that arises in the final stage production of steel coils. Steel coils can be required
to galvanised, i.e. coated with a zinc layer to protect them against air and mosture. The steel coils are coated in batches
where the coils in each batch are welded end to end to produce one continous strip of steel. This strip is then processed
through the galvanizing line with no downtime between the individual coils that compose the strip.

The sequence of the individual coils in the strip determines how much wastage of steel occurs as a result of the galvansing
line needing to be recalibrated between coils. When the line transitions from coating one coil to the next, wastage occurs
because the transition period of the line results in the beginning of the next coil being treated at suboptimal parameters.
This can produce a section of the coils which is inferiror or unsaleable.

However, because of the relative settings required for different pairs of coils, the transition periods can be shortened
by sequencing the coils such that consecutive pairs of coils have less wastage.

Addtionally, because of phsyical differences in the individual coils, such as steel grade, some coils cannot be sequenced consecutively after other coils.

Moreover the order in which a pair of coils is consecutively sequenced can result in different amounts of wastage.

The complete choice of consecutive pairs forms a sequence, and the goal here to select a sequence to minimise aggregate wastage.

The solver implemented in this repo uses a graph theoretic formulation of the sequencing problem and finds the optimal sequence for a batch coils by using a branch and bound algorithm variant.

Details of the graph theoretic formulation of the problem, and the branch and bound algorithm used to solve it, 
can be found in the docs here - INSERT INTERNAL LINK



## Table of Contents

- [Installation](#installation)
- [Problem Instances](#problem-instances)
- [Usage](#usage)
- [Problem Description and Solution Approach](#problem-description-and-solution-approach)
- [Codebase Structure](#codebase-structure)
- [Results obtained used this solver](#results-obtained-used-this-solver)
- [Ideas for optimization algorithm improvement](#ideas-for-optimization-algorithm-improvement)



## Installation

Git clone the repo to gain access to the code. I use the conda to manage virtual environemnts and have provided
an environment.yml file to create a conda virtual environment with the required dependencies. I also created a pip
compatible requirements.txt file in the dependencies directory, but an attempt to create a virtualenv virtual environment using pip failed due to pip being unable to find all required packages.

To clone the repo and setup the required conda virtual enviroment execut the following commands:

'''
git clone https://github.com/shmulib/CGLSP.git
cd CGLSP
conda env create -f dependencies\environment.yml'''

## Problem Instances

This CGLSP sequencing problem comes from research Spanish academics conducted to aid a Spanish steel manufacturing company.

I've provided the paper they wrote about their research on the CGLSP problem in the CGLSP_academic research directory of this repo. The paper is the file - Sequencing jobs with asymmetric costs and transition constraints.pdf

The authors also provide 30 real problem instances derived from actual batches of steel coils required to be sequenced at the steel manufacturer.

These 30 instances are provided in this repo in the problem_instances/CGLSP_instances/data directory.

Each problem instance file is labelled cgl_{num_coils}.txt where the num_coils is the number of steel coils required
to be galvanised in that batch.

The contents of the problem instance files are cost matrices for the batch where entry (i,j) is the cost of sequencing
coil j directly after coil i. All costs are non-negative except for pairs of coils that can't be sequence directly after
each other, where the cost is -1 to indicate infeasibility.

The smallest of the problem instances provided by the Spanish researches is cgl_17, containing 17 coils to be sequenced.
Using this solver I have solved cgl_17 to optimality. I'm yet to be able to solve the other instances to optimality (the solver doesn't terminate), but I have several ideas for improving the branch and bound algorithm that should allow larger instances to be solved at all, and smaller instances to be solved faster.

Further details of the problem instances are provided in the problem_instances/CGLSP_instaces/README.md file which was
provided by the Spanish academics who shared the instances publicly.

You can also read about the problem instances in this paper written by the same academics, which is 
provided in this repo in CGLSP_academic_research/Problem_instances_dataset_of_a_real-world_sequencing_problem.pdf 

I have also provided another problem instance of the same graph theoretic optimization problem, i.e. Asymmetric Travelling
Salesman Problem. This instance is br17 from the ASTP problem instances in the TSPLIB95 database. The instance is located
in problem_instances/TSPLIB_instances/br17.atsp

The TSPLIB95 database contains problem instances of a variety of different TSP problem variants including ATSP as well as optimalsolutions for the instances where they are known.

The br17 instance has been provably solved to optimality. I have used this solver to solve the br17 instance to optimality as a means verifying correctness.

## Usage

The entry point to the solver is script CGLSP.py in the root directory.

I've implemented a command line interface to run the solver using this script, for selected problem instances that I have successfully solved to optimality, i.e. cgl_17 and br17.

You can use the command line interface as follows to run the solver for these instances:




## Problem Description and Solution Approach


Problem Description in context
Graph theory formulation
Mathematical description of solution
Description of how the algorithm is implemented in code -



## Codebase Structure

 structure of code base ..

## Results obtained used this solver



Results so far
Problems encountered - GCGLPS_26 can't find tight enough LBs
                    - TSPLIP br17 is solved exactly, but tree grows relatively large
                    - even though optimal solution is found, because branching results in subproblems with very low LB, not feasible sols to CGLSP, only to the relaxation


## Ideas for optimization algorithm improvement

Work still to be done

































