# CGLSP (Continuous Galvanizing Line Sequencing Problem)

Documentation to include:
* Problem Description in context
* Graph theory formulation
* Mathematical description of solution
* Description of how the algorithm is implemented in code - structure of code base ..
* How to setup env to run code
* How to run the solver for instances ->  navigate to root CGLSP dir and then run CGLSP.py with problem type arg
* Where the results are stored
* Work still to be done
* Results so far
* Problems encountered
  * GCGLPS_26 can't find tight enough LBs
  *TSPLIP br17 is solved exactly, but tree grows somewhat large even though optimal solution is found early on, because branching results in 
   subproblems with very low LB. The obtained optimal MAP solutions are not CGLSP feasible


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

Provide instructions for how to install your project. Include any prerequisites and steps needed to get your project up and running.

Example:
```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
pip install -r requirements.txt
