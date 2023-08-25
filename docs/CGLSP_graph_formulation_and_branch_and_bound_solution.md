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
 
Applied Problem: 
I found a real sequencing problem for the galvanizing of steel coils. Spanish academics published research about this problem where they were employed by a Spanish steel manufacturer. (I've included the paper in the git repo).

The problem is that a batch of steel coils needs to be treated with a zinc coating. The coils are welded end to end
and pushed through a continuous production line. The sequence of the coils affects the amount of wastage of steel incurred at the beginning of coating each coil. 

The reason this wastage occurs is due to the specific parameters of the coating pipeline required for each coil and the requirement that the coils be coated continuously. This creates an avoidable period of transition at the beginning of coating each coil, in which the parameters of the pipeline are gradually modified to the ideal values for the currently being coated coil, from those used/ideal for the previous coil. During this period of transition the coils may not be treated ideally and this may produce inferior or unsaleable steel that has to be sold at much lower rates, if it can be sold at all.

The objective is then, of course, to sequence the coils in such a way as to avoid as much wastage as possible.

The different sequences are associated with varying levels of wastage because the wastage incurred for different consecutive pairs of coils varies. The order within the consecutive pairs, i before j, or vice versa, can also incur different amounts of wastage, i.e. the costs are not symmetric.

Moreover, not all sequences are allowed as some coils may not be coated consecutively after other coils, due to physical constraints like relative steel grades, etc. I'm not sure if these constraints are also asymmetric in practice.


Graph Theoretic Formulation:


This sequencing problem can be formulated as finding the miminum cost Hamiltonian path in an incomplete asymmetric weighted graph.

The


The theoretical optimization problem can be formulated as finding the minimum cost Hamiltonian path in an asymmetric, incomplete graph.

It's possible to formulate this problem as an Asymmetric Travelling Salesman Problem (ASTP) (min cost Hamiltonain cycle, as opposed to, path) in an incomplete graph, by adding a dummy node (coil) to the graph formulation and adding edges to and from the dummy node to every other node, with zero cost.This reformulation is what I've done in my solution. 

I then solve the resulting ASTP exactly using a branch and bound variant.

Lower Bounding:

 Lower bounds are generated on the subproblems by solving a relaxation of the ASTP, referred to as the Modified Assignment Problem (MAP).

 The classical Assignment Problem (AP) involves, in the balanced case, assigning a set of n workers to n tasks, such that each worker is assigned to one task, and each task is completed by one worker. The costs of the specific assignment of individual workers to specific tasks varies, and so less total cost can be incurred by some overall assignments than others. In the simplest variant of the AP, each worker can be assigned to each task, although of course, we are interested in a variant in which not all assignments are feasible. The graph formulation of the Assignment Problem involves finding a min cost collection of subtours or subcycles within the graph. Of course a Hamiltonian cycle is also a subtour, just one in which all the nodes are included, so the optimal cost for the Assignment Problem is a lower bound to the optimal cost Hamiltonian cycle on the same graph. We utilize this to lower bound subproblems of the ASTP. We solve instances of the Assignment Problem, where some edges have already been fixed, included/excluded, corresponding to the pairs of coils included/excluded in the subproblems of our branch and bound tree. (These Assignment problems are referred to as *modified* because of the inclusion/exclusion of edges) 

It is also possible to generate lower bounds for subproblems of the ASTP using other methods such as cost reduction methods, but I haven't implemented those yet.

Upper Bounding:

We also use the cost of the optimal solutions of the Modified Assignment Problems of our subproblems as upper bounds for the lowest cost sequence of coils.

The cost of the optimal solution of the Modified Assignment Problem is an upper bound on the ASTP, whenever the optimal solution is a Hamiltonian cycle, because then it is also a feasible solution of the ASTP. Whenever we find ASTP feasible MAP optimal solutions that are better than our previously best discovered solution we can tighter our upper bound.

Branching:

Choice of decision variables to branch on:
