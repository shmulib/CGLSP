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

Git clone the repo to gain access to the code. I useconda to manage virtual environemnts and have provided
an environment.yml file to create a conda virtual environment with the required dependencies. I also created a pip
compatible requirements.txt file in the dependencies directory, but an attempt to create a virtualenv virtual environment using pip failed due to pip being unable to find all required packages.

To clone the repo and setup the required conda virtual enviroment execute the following commands (note the \ for Windows):

```
git clone https://github.com/shmulib/CGLSP.git
cd CGLSP
conda env create -f dependencies\environment.yml
```

## Usage

How to run the solver for instances ->  navigate to root CGLSP dir and then run CGLSP.py with problem type arg


Where the results are stored

## Problem Description and Solution Approach


Problem Description in context
Graph theory formulation
Mathematical description of solution
Description of how the algorithm is implemented in code -

## Problem Instances

 CGLSP and TSPLIB

## Codebase Structure

 structure of code base ..

## Results obtained used this solver


Results so far
Problems encountered - GCGLPS_26 can't find tight enough LBs
                    - TSPLIP br17 is solved exactly, but tree grows relatively large
                    - even though optimal solution is found, because branching results in subproblems with very low LB, not feasible sols to CGLSP, only to the relaxation


## Ideas for optimization algorithm improvement

Work still to be done

























