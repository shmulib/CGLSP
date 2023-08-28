
# Graph Theoretic Formulation of CGLSP

The CGLSP sequencing problem can be formulated as a graph optimization problem of finding a minimum cost Hamiltonian path on an incomplete asymmetric graph, or digraph.

The nodes in the graph are the coils to be sequenced, and the directed edge from node i to node j represents galvansing coil j directly after coil i. The weight of this edge is the cost or wastage inccured when coil j is galvanised directly after coil i. 

The graph is incomplete because not all pairs of coils can be galvanised directly after each other, and therefore there are missing edges in the graph.

The asymmetry arises because the wastage incurred from galvanising coil j directly after coil i, may be different from the wastage incurred from galvansing the pair in the reverse order, i.e. coil i directly after coil j.

A Hamilitonian path in a graph is a path that starts at some node and then travels along the edges of the graph visiting every node without repeating edges. Note, that unlike a Hamiltonian cycle, a Hamiltonian path does not end at the node at which it started.

As there are possibly multiple Hamlitonian paths in a given graph, there exists a graph optimization problem of finding a minimum weight Hamilitonian path in a graph, which means finding a Hamiltonian path, where the sum of the weights of the edges in the path is minimised over all Hamiltonian paths in that graph.

In the context of the (di)graph representing the CGSLP sequencing problem, a Hamiltonian path is a valid sequencing of the coils to be galvanised. A minimum weight Hamiltoninan path in the CGLSP graph represents a valid sequence of coils that incurs the least aggregate wastage.

Hence, by representing the CGLSP sequencing problem using this graph theory formulation, we can find a valid sequence of coils with least aggregate wastage, by finding a minimum weight Hamiltonian path in its graph.

In order to solve this graph optimization problem, the optimization problem is transformed into a slightly different optimization problem, with the same solution, on a modified/augmented graph.

The problem of finding a minimum cost Hamiltoniain path on a asymmetric graph is not usually studied directly. Instead, a minimum cost Hamiltonian cycle is sought, i.e. a path that starts and ends at the same node in the graph. However, one can find a minimum cost Hamiltonian path in any graph, just by adding an additional dummy node in the graph and connecting it to all the other nodes (in both directions) with edges with zero weight. A minimum weight Hamiltonian cycle on this graph, can then be trivially converted into a minimum weight Hamiltonian path on the orignal graph.

The problem of finding a minimum weight Hamiltonian cycle on an assymetric graph is more commonly known as the Assymetric Travelling Salesman Problem. This is a very well studied problem and many approaches for solving it have been devised.

Usually though, the problem is formulated using complete graphs that ensure a Hamiltonian cycle exists. In an incomplete graph, there is no guarantee that a Hamiltonian cycle exists. The incomplete graph variant is therefore much harder to solve as not only does one have to minimize the cost of the Hamiltonian cycle, but one has to even determine if there are any Hamiltonian cycles in the graph.

In the next section, we explain the branch and bound algorithm variant, the solver implented in this repo, uses to find a minimum weight Hamiltonian cycle on the augmented graph with the dummy node (coil).  Upon termination the solver uses this Hamiltonian cycle to extract a minimum weight Hamiltonian path on the original graph, and consequently, finds the optimal sequence for galvanising the coils with the minimum aggregate wastage.

# Branch and Bound Solution

The optimization approach that we use to solve the CGLSP sequencing problem, upon termination, finds the optimal solution, and is therefore what is known as an "exact" method. This is in contrast to another commonly used class of optimization techniques, heuristics or approximation methods, that aren't guaranteed to find optimal solutions to the problems they are solving, instead they find somewhat optimal solutions. However, these methods are usually faster, and are also necessary when solving optimization problems for which finding the optimal solution is intractable. The specific exact method that we use is a variant of branch and bound.

Generically, a branch and bound algorithm, when it works well, is an efficient search of the solution space of the optimization problem. Branch and bound algorithms branch the original optimization problem by recursively partitioning the solution space into smaller subsets, hence obtaining subproblems, which are easier to optimize over then the full optimization problem. When branching, this partitioning of a subproblem is achieved by creating child subproblems that have decision variables fixed relative to their parent subproblem, in such a way that all solutions in the parent subproblem exist collectively in the child subproblems and the solution space of the subproblems are entirely distinct (mutually exclusive) of each other. The efficiency of a branch and bound algorithm is then determined, for a given choice of a branching strategy, by the bounding that is performed. There are two types of bounds required, an upper bound and lower bounds. The upper bound is an upper bound on the optimal solution of the full optimization problem. For a minimization problem, the cost of any feasible solution of the optimization problem is an upper bound - because if a feasible solution has been found with a specific cost, the optimal cost cannot be higher than this. Unlike, the upper bound, for which the branch and bound algorithm keeps track of one upper bound value at time, only updating it when a feasible solution with lower cost is found, the lower bounds that are tracked are lower bounds on the optimal solution of each subproblem branched to. By obtaining lower bounds for the optimal solution of subproblems, where the the lower bound is higher then best found solution so far for the full optimization problem, those subproblems can be pruned from the branch and bound tree, since the optimal solution for the full optimization problem cannot be a feasible solution belonging to that subproblem (in the case where the upper bound is equal to the lower bound for a subproblem, an optimal solution of the full optimization problem could be an optimal solution of the subproblem, but in this case we still don't need to branch this subproblem because it can't contain a better solution than the best feasible solution obtained thus far). In this way, by obtaining feasible solutions with fairly low cost, and creating subproblems by branching, for which a tight lower bound on their optimal solution can be found, a large proportion of the feasible solution space does not need to be explicitly searched while obtaining the optimal solution to the full optimization problem. 

In practice therefore, the quality of a branch and bound algorithm is determined by the choice of branching strategy, which consists of two components, firstly how the decision variables are fixed in a parent subproblem to obtain the child subproblems, i.e. which subproblems are created, and secondly the order in which the supbroblems are explored, as well as the mechanisms used to obtain tight lower and upper bounds. If the upper bounds are not low enough, then the likely outcome is that the lower bounds on subproblems will be lower then obtained upper bound, in which case a very large number of subproblems will be created. Alternatively, even if the optimal solution of the full optimization problem is found, i.e. the best upper bound possible, because this actually isn't known until subproblems can be ruled out as not having a more optimal solution, if the lower bounds obtained on the subproblems are lower than that upper bound, i.e. the optimal solution, then equally, a large number of subproblems will be created.

In the context of finding a minimum weight Hamiltonian cycle on a graph, the branch and bound subproblems have edges of the graph which cannot be part of the Hamiltonian cycles found for that subproblem (excluded edges), and/or edges of the graph which have to be included in the Hamiltonian cycles found for that subproblem (included edges).

For each subproblem, lower bounds are obtained for the solution on the subproblem



Lower bounds for the optimal solution can be obtained by solving a closely related optimization problem to the original optimization problem in which constraints on the solution space have been relaxed. The feasible solution space for this relateed optimization problem is therefore a superset of the feasible solution space for the original optimization problem. The result is that the optimal solution of the less constrained related optimization problem is at least as optimal as the optimal solution of the orignal optimization problem. It therefore provides a lower bound on the optimal solution of the original optimization problem.

In the context of the CGLSP, these upper bounds are therefore feasible solutions - so any valid sequence of coils, i.e. sequences that don't contain consecutive pairs of coils that can't physically be galvanised after each other. In the associated augmented graph, this corresponds to any Hamiltonian cycle that exists in the graph. 

The lower bounds are found by finding the optimal choice of edges in the graph such that every node has an in and out degree of 1, i.e. is connected to exactly two edges, as in a Hamiltonian cycle, but we relax the constraint that this collection of edges needs to form a Hamiltonian cycle. Instead the collection of edges can consist of multiple subcycles in the graph that start and end at the same node, but don't individually visit every node in the graph. This relaxation of the constraint that the choice of edges needs to form a Hamiltonian cycle, means that we are now solving the original optimization problem on a new feasible solution space that contains as a (proper) subset the set of all Hamiltonian cycles on the graph. Consequently, the optimal choice of edges, i.e. the solution, of this relaxation optimization problem is at least as optimal, as the optimal Hamiltonian cycle of the graph.  Hence the cost of this solution is a lower bound on the optimal cost of Hamiltonian cycle.




Lower Bounding:

 Lower bounds are generated on the subproblems by solving a relaxation of the ASTP, referred to as the Modified Assignment Problem (MAP).

 The classical Assignment Problem (AP) involves, in the balanced case, assigning a set of n workers to n tasks, such that each worker is assigned to one task, and each task is completed by one worker. The costs of the specific assignment of individual workers to specific tasks varies, and so less total cost can be incurred by some overall assignments than others. In the simplest variant of the AP, each worker can be assigned to each task, although of course, we are interested in a variant in which not all assignments are feasible. The graph formulation of the Assignment Problem involves finding a min cost collection of subtours or subcycles within the graph. Of course a Hamiltonian cycle is also a subtour, just one in which all the nodes are included, so the optimal cost for the Assignment Problem is a lower bound to the optimal cost Hamiltonian cycle on the same graph. We utilize this to lower bound subproblems of the ASTP. We solve instances of the Assignment Problem, where some edges have already been fixed, included/excluded, corresponding to the pairs of coils included/excluded in the subproblems of our branch and bound tree. (These Assignment problems are referred to as *modified* because of the inclusion/exclusion of edges) 

It is also possible to generate lower bounds for subproblems of the ASTP using other methods such as cost reduction methods, but I haven't implemented those yet.

Upper Bounding:

We also use the cost of the optimal solutions of the Modified Assignment Problems of our subproblems as upper bounds for the lowest cost sequence of coils.

The cost of the optimal solution of the Modified Assignment Problem is an upper bound on the ASTP, whenever the optimal solution is a Hamiltonian cycle, because then it is also a feasible solution of the ASTP. Whenever we find ASTP feasible MAP optimal solutions that are better than our previously best discovered solution we can tighter our upper bound.

Branching:

Choice of decision variables to branch on:
