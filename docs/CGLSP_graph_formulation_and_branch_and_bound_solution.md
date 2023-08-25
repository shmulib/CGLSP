# Graph Theoretic Formulation of CGLSP

The CGLSP sequencing problem can be formulated as a graph theory optimization problem of finding a minimum cost Hamiltonian path on an incomplete asymmetric graph, or digraph.

The nodes in the graph are the coils to be sequenced, and the directed edge from node i to node j represents galvansing coil j directly after coil i. The weight of this edge is the cost or wastage inccured when coil j is galvanised directly after coil i. 

The graph is incomplete because not all pairs of coils can be galvanised directly after each other, and therefore there are missing edges in the graph.

The asymmetry arises because the wastage incurred from galvanising coil j directly after coil i, may be different from the wastage incurred from galvansing the pair in the reverse order, i.e. coil i directly after coil j.

A Hamilitonian path in a graph is a path that starts at some node and then travels along the edges of the graph visiting every node without repeating edges. Note, that unlike a Hamiltonian cycle, a Hamiltonian path does not end at the node at which it started.

As there are possibly multiple Hamlitonian paths in a given graph, there exists a graph optimization problem of finding a minimum weight Hamalitonian path in a graph, which means finding a Hamiltonian path, where the sum of the weights of the edges in the path is minimised over all Hamiltonian paths in that graph.

In the context of the (di)graph representing the CGSLP sequencing problem, a Hamiltonian path is a valid sequencing of the coils to be galvanised. A minimum weight Hamiltoninan path in the CGLSP graph represents a valid sequence of coils that incurs the least aggregate wastage.

Hence, by representing the CGLSP sequencing problem using this graph theory formulation, we can find a valid sequence of coils with least aggregate wastage, by finding a minimum weight Hamiltonian path in its graph.

In order to solve this graph theory optimization problem, the optimization problem is transformed into a slightly different optimization problem with the same solution on modified/augmented graph.

The problem of finding a minimum cost Hamiltoniain path on a asymmetric graph is not usually studied directly. Instead, a minimum cost Hamiltonian cycle is sought, i.e. a path that starts and ends at the same node in the graph. However, one can find a minimum cost Hamiltonian path in any graph, just by adding an additional dummy node in the graph and connecting it to all the other nodes (in both directions) with edges with zero weight. A minimum weight Hamiltonian cycle on this graph, can then be trivially converted into a minimum weight Hamiltonian path on the orignal graph.

The problem of finding a minimum weight Hamiltonian cycle on an assymetric graph is more commonly known as the Assymetric Travelling Salesman Problem. This is very well studied problem and many approaches for solving it have been devised.

Usually though, the problem is formulated using complete graphs that ensure a Hamiltonian cycle exists. In an incomplete graph, there is no guarantee that a Hamiltonian cycle exists. The incomplete graph variant is therefore much harder to solve as not only does one have to minimize the cost of the Hamiltonian cycle, but one has to even find Hamiltonian cycles to begin with.

In the next section, we explain the branch and bound algorithm variant the solver implented in this repo uses to find a minimum weight Hamiltonian cycle on the augmented graph with the dummy node, which upon termination finds a minimum weight Hamiltonian path on the original graph and consequently, the optimal sequence for galvanising the coils which has the minimum aggregate wastage.

# Branch and Bound Solution

The optimization approach that we use to solve the CGLSP sequencing problem, upon termination, finds the optimal solution, and is therefore what is known as an "exact" method. The is contrasted to another commonly used class of optimization techniques that aren't guaranteed to find optimal solutions to the problems they are solving, but are usually faster and also are necessary when solving the optimization problem to optimality is intractable.

Specifically, we use a branch and bound algorithm variant. Branch and bound, when it works well, is effectively an efficient search of the solution space. Branch and bound algorithms recursively partition the solution space into smaller subsets of the solution space and solve the optimization problem on those subsets. The partioning is achieved by branching on the subproblem currently being processed. Branching means creating child subproblems that have decision variables fixed in their parent subproblem in such a way that all solutions in the parent subproblem exist collectively in the child subproblems and the solution space of the subproblems are entirely distinct (mutually exclusive) of each other. 

Less abstractedly, in the context of finding a minimum weight Hamiltonian cycle on a graph, subproblems involve finding minimum weight Hamiltonian cycles on the graph where edges of the graph either cannot be part of the Hamiltonian cycles found for that subproblem (excluding edges), or edges of the graph have to be included in the Hamiltonian cycles found for that subproblem (including edges).

The way that branch and bound can effeciently search the solution space for the optimal solution is by using upper and lower bounds for the optimal solution.

An upper bound for the optimal solution (in the case of a minimization problem, like ours) is any feasible solution of the optimization problem. 

Lower bounds for the optimal solution can be obtained by solving a closely related optimization problem to the one trying to be solved in which constraints on the solution space have been relaxed and therefore the feasible solution space for this relateed optimization problem is a superset of the feasible solution space for the original optimization problem.

In the context of the CGLSP, these upper bounds are provided by feasible solutions that are any valid sequence of coils, i.e. sequences that don't contain consecutive pairs of coils that can't physically be galvanised after each other. In the associated augmented graph, this corresponds to any Hamiltonian cycle that exists in the graph. 

The lower bounds are found by finding the optimal choice of edges in the graph such that every node has an in and out degree of 1, i.e. is connected to exactly two edges, as in a Hamiltonian cycle, but we relax the constraint that this collection of edges needs to form a Hamiltonian cycle. Instead the collection of edges can consist of multiple subcycles in the graph that start and end at the same node, but don't individually visit every node in the graph. As the set of all such collections of edges in the graph that visits every node, where the collections can consists of multiple subcycles, contains within in it the subset of collections where each collection of edeges is a Hamiltonian cycle (a Hamiltonian cylce is just a subcycle that actually visits every node), the minimum weight collection over all collections that consists of subcycles, has a weight that is at least as low as the minimum weight collection that is a Hamiltonian cycle. As such by find this optimal collection of edges that consists of (potentially) multiple collections, we have found a lower bound on the minimum weight Hamiltonian cycle.




Lower Bounding:

 Lower bounds are generated on the subproblems by solving a relaxation of the ASTP, referred to as the Modified Assignment Problem (MAP).

 The classical Assignment Problem (AP) involves, in the balanced case, assigning a set of n workers to n tasks, such that each worker is assigned to one task, and each task is completed by one worker. The costs of the specific assignment of individual workers to specific tasks varies, and so less total cost can be incurred by some overall assignments than others. In the simplest variant of the AP, each worker can be assigned to each task, although of course, we are interested in a variant in which not all assignments are feasible. The graph formulation of the Assignment Problem involves finding a min cost collection of subtours or subcycles within the graph. Of course a Hamiltonian cycle is also a subtour, just one in which all the nodes are included, so the optimal cost for the Assignment Problem is a lower bound to the optimal cost Hamiltonian cycle on the same graph. We utilize this to lower bound subproblems of the ASTP. We solve instances of the Assignment Problem, where some edges have already been fixed, included/excluded, corresponding to the pairs of coils included/excluded in the subproblems of our branch and bound tree. (These Assignment problems are referred to as *modified* because of the inclusion/exclusion of edges) 

It is also possible to generate lower bounds for subproblems of the ASTP using other methods such as cost reduction methods, but I haven't implemented those yet.

Upper Bounding:

We also use the cost of the optimal solutions of the Modified Assignment Problems of our subproblems as upper bounds for the lowest cost sequence of coils.

The cost of the optimal solution of the Modified Assignment Problem is an upper bound on the ASTP, whenever the optimal solution is a Hamiltonian cycle, because then it is also a feasible solution of the ASTP. Whenever we find ASTP feasible MAP optimal solutions that are better than our previously best discovered solution we can tighter our upper bound.

Branching:

Choice of decision variables to branch on:
