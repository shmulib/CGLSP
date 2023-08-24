import numpy as np
import queue
from src.node import Node
from src.MAP_solver import PossibleOverflowException


class BnB_Tree:
    def __init__(self, root_cost_matrix, instance_size, update_frequency):
        self.root_cost_matrix = root_cost_matrix
        self.instance_size = instance_size
        self.root_node = Node(
            root_cost_matrix,
            instance_size=instance_size,
            included_edges=[],
            excluded_edges=[],
            lower_bound=0,
        )
        self.unpruned_nodes = queue.PriorityQueue()
        self.best_cost = np.inf
        self.best_solution = []
        self.explored_subproblems = 0
        self.optimal_subproblem_solutions_found = 0
        self.pruned_subproblems = 0
        self.branched_subproblems = 0

        self.update_frequency = update_frequency

    def solve(self):

        # Process the root node
        self.explored_subproblems += 1

        # Find initial feasible solution (using a heuristic solve)
        # UNCOMMENT when you have implemented the heuristic solver
        # self.best_cost, self.best_solution = self.root_node.get_feasible_sol()

        # best cost of -1 is returned when there are no feasible solutions to CGLSP
        if self.best_cost == -1:
            return self.best_cost, self.best_solution

        # Find an initial lower bound on CGLSP using a cost reduction method
        self.root_node.get_cost_reduction_lower_bound()

        # if the determined lower bound by cost reduction is the
        # the same as the best cost found so far
        # then our initial feasible solution is optimal
        if self.root_node.lower_bound == self.best_cost:
            self.optimal_subproblem_solutions_found += 1
            return self.best_cost, self.best_solution

        # otherwise, we attempt to tighten the lower bound by solving
        # the MAP relaxation of the CGLSP:
        self.root_node.solve_MAP()

        # check if MAP relaxation was solved without any possible integer
        # overflow issues
        if self.root_node.MAP_solve_status == "POSSIBLE_OVERFLOW":
            raise PossibleOverflowException(
                "MAP Solver couldn't solve MAP relaxation for the root node. \
                 Failed with a possible integer overflow"
            )

        # if the MAP optimal solution established a tighter lower bound that
        # is the same as the best found cost so far then we've already found the
        # optimal solution
        if self.root_node.lower_bound == self.best_cost:
            self.optimal_subproblem_solutions_found += 1
            return self.best_cost, self.best_solution

        # Otherwise, if the MAP lower bound is lower than the current best cost
        # (as was the cost reduction lower bound), then either

        # 1. Since the MAP optimal solution is the optimal solution for
        #   a relaxation of the CGLSP, if the MAP optimal solution is a
        #   feasible solution to the CGLSP, then the MAP optimal solution
        #   is an optimal solution for the CGLSP
        elif self.root_node.MAP_sol_CGLSP_feasible():
            self.optimal_subproblem_solutions_found += 1
            self.best_cost = self.root_node.MAP_best_cost
            self.best_solution = self.root_node.MAP_solution

            return self.best_cost, self.best_solution

        # 2. otherwise if the MAP optimal solution is not CGLSP feasible,
        #    then the best solution may yet not have been found, so we need
        #    to explore subproblems by branching (uing the MAP solution to
        #    branch)
        else:
            node_priority = self.root_node.lower_bound
            self.unpruned_nodes.put((node_priority, self.root_node))

        # while there are still subproblems with potentially better solutions
        # than the best solution obtained so far, explore those unpruned subproblems
        while not self.unpruned_nodes.empty():

            # if a subproblem is in the queue that's because it needs to be explored
            # Its lower bound is lower than the currently best known solution
            # and its MAP solution (relaxation) is not feasible for CGLSP because it
            # consists of subtours
            # We need to branch the current subproblem
            # - i.e. create children subproblems and then iterate over the children
            # subproblems

            # obtain the current unpruned subproblem with the lowest lower bound
            # by popping the min item from the unpruned nodes priority queue
            cur_node = self.unpruned_nodes.get()[1]

            self.branched_subproblems += 1

            # if we have branched a multiple of update_frequency times
            # output solver progress updates to the console

            if self.branched_subproblems % self.update_frequency == 0:
                dashed_line = "-" * 80
                print(dashed_line)
                print(f"Solution progress after branching {self.branched_subproblems} times: \n")
                print("Min cost found so far: ", self.best_cost)
                print("Explored subproblems: ",
                      self.explored_subproblems)
                print("Upper bound updates: ",
                      self.optimal_subproblem_solutions_found)
                print("Pruned subproblems: ",
                      self.pruned_subproblems)
                print("Branched supbroblems: ",
                      self.branched_subproblems)
                print("Current subproblems still required to process: ",
                      self.unpruned_nodes.qsize())

            # branch the current subproblem just popped of the queue
            children_nodes = self.branch(cur_node)

            # for each of the branched subproblems, process them
            for node in children_nodes:

                self.explored_subproblems += 1

                # First we attempt to prune the node from branch and bound tree by
                # calculating a tighter lower bound than the lower bound
                # inherited from its parent, using cost reduction
                # We will update the known lower bound for this subproblem if the cost
                # reduction lower bound is higher than the current lower bound
                node.get_cost_reduction_lower_bound()

                # if the lower bound determined by cost reduction is at least as
                # high as the cost of the best known solution, then there is not a more
                # optimal solution in this subtree, in which case we can prune it
                if node.lower_bound >= self.best_cost:
                    self.pruned_subproblems += 1
                    continue

                # otherwise, if the initial lower bound found using cost reduction
                # is lower than our known best cost, then solve the Modified Assignment
                # problem for this subproblem.
                # The obtained optimal MAP solution for this subproblem could result in:
                #   1. Pruning the subproblem, if the MAP optimal cost which is a lower
                #      bound on the subproblem, is at least as high as the best cost
                #      known so far, as then this subtree can't contain the optimal
                #      solution, or
                #   2. Finding a new best solution if the MAP optimal solution is CGLSP
                #      feasible and has lower cost then our current best cost,
                #      as well as pruning the subproblem, because then the MAP optimal
                #      solution is the optimal solution for this subproblem and so we
                #      don't need to explore the subproblem further, or
                #   3. The need to branch this subproblem further if we can't
                #      establish a higher lower bound on the subproblem than
                #      our current best solution

                node.solve_MAP()

                # Check if there is no feasible solution for the MAP relaxation of the
                # subproblem. If this is the case then there is no feasible solutions
                #  for the subproblem at all and therefore the subproblem can be pruned
                if node.MAP_solve_status == "INFEASIBLE":
                    self.pruned_subproblems += 1
                    continue

                # check if MAP relaxation was solved without an integer overflow issue
                if node.MAP_solve_status == "POSSIBLE_OVERFLOW":
                    raise PossibleOverflowException(
                        "MAP Solver couldn't solve MAP relaxation for this subproblem. \
                                              Failed with a possible integer overflow"
                    )

                # otherwise, if a feasible solution for the MAP relaxation of the
                # subproblem was found
                # and if the (new) lower bound found for this subproblem is at least as
                # high as the cost of the best known solution, then there is not a more
                # optimal solution in this subtree
                if node.lower_bound >= self.best_cost:
                    self.pruned_subproblems += 1
                    continue

                # otherwise, if the MAP lower bound is lower than the current best
                # cost (and so is the cost reduction lower bound)
                # then if:
                #        1. the MAP found a feasible solution to the CGLSP, then this
                #           solution is the best known solution so far
                #           and this solution is the best for this subproblem,
                #           so we don't need to explore it further
                #        2. otherwise, the best solution may be in this subset of the
                #           solution space, in which case we need to use the MAP
                #           solution to branch this subproblem
                else:
                    if node.MAP_sol_CGLSP_feasible():
                        self.optimal_subproblem_solutions_found += 1

                        self.best_cost = node.MAP_min_cost
                        self.best_solution = node.MAP_solution

                        # remove all subproblems from queue with lower bound above
                        # the new best cost
                        self.prune_queue()

                    else:
                        # if the MAP solution wasn't feasible then we need to
                        # branch this subproblem
                        node_priority = node.lower_bound
                        self.unpruned_nodes.put((node_priority, node))

        # Output fianl solution statistics once the optimal solution has been found
        dashed_line = "-" * 80
        print(dashed_line)
        print(f"Solution statistics at end of solve: \n")
        print("Explored subproblems: ",
              self.explored_subproblems)
        print("Upper bound updates: ",
              self.optimal_subproblem_solutions_found)
        print("Pruned subproblems: ",
              self.pruned_subproblems)
        print("Branched supbroblems: ",
              self.branched_subproblems)
        print("Current subproblems still required to process: ",
              self.unpruned_nodes.qsize())

        return self.best_cost, self.find_subtours(self.best_solution)[0]

    def branch(self, node):
        # takes a subproblem that may contain the optimal solution to CGLSP
        # and branches the subproblem based on the subtour of its MAP optimal solution
        # with the least edges in common with the included edges of the subproblem

        # get the list of non included edges of minimal subtour
        minimal_subtour_non_included_edges = self.minimal_subtour_edges(
            node.included_edges, node.MAP_solution
        )

        # using this minimal subtour branch the subproblem
        num_children_nodes = len(minimal_subtour_non_included_edges)
        children_nodes = []
        for i in range(num_children_nodes):

            # determine the edges to fix in each of the branched subproblems, child
            # subproblem, j=1...len(minimal_subtour_non_included_edges)
            # for child subproblem j,
            # exclude edge j of the minimal_subtour_non_included_edges
            # and the current subproblem excluded edges, and
            # include edges 1...j-1 of the minimal_subtour_non_included_edges
            # and the current subproblem included edges

            new_included_edges = minimal_subtour_non_included_edges[0:i]
            new_excluded_edge = minimal_subtour_non_included_edges[i: i + 1]
            child_included_edges = new_included_edges + node.included_edges
            child_excluded_edges = new_excluded_edge + node.excluded_edges

            # create the new child subproblem
            child_node = Node(
                cost_matrix=self.root_cost_matrix,
                instance_size=self.instance_size,
                included_edges=child_included_edges,
                excluded_edges=child_excluded_edges,
                lower_bound=node.lower_bound,
            )
            # append it to the list of child subproblems to be process by the branch
            # and bound algorithm next
            children_nodes.append(child_node)

        # return the children nodes in the order of most number of new included edge
        # restrictions
        # we will process them in this order, as the more constrained the subproblems
        # are, the more likely they are to contain optimal solutions without as
        # much additional branching
        # which will allow us to prune the branch and bound tree earlier
        # to try to prevent it from growing very large

        return children_nodes[::-1]

    def minimal_subtour_edges(self, node_included_edges, node_MAP_sol):
        # for each subtour in MAP solution, find how many non included edges it has
        # return edges of subtour with minimum number of edges not in the nodes included
        # edges
        # ideally order the edges according to Carpaneto criteria, but for now we will
        # just return them in order of the tour as per simplified Laporte version

        # obtain all subtours of the MAP solution
        subtours = self.find_subtours(node_MAP_sol)

        # the subtour with the minimum number of non included edges must have less than
        # a full tour of non included edges
        # as the subtour itself already has less than a full tour of edges
        # hence we set this as the upper bound for minimizing over the subtours
        min_non_included_edges = self.instance_size

        # iterated through all the subtours and find the subtour with the minimum number
        # of edges not already included in the current subproblem
        for subtour in subtours:
            subtour_non_included_edges = set(
                subtour) - set(node_included_edges)
            num_non_included_edges = len(subtour_non_included_edges)
            # if the current subtour has the least number of non included edges so far
            if num_non_included_edges < min_non_included_edges:
                # updated the least number of non included edges in a subtour
                min_non_included_edges = num_non_included_edges
                # get a list of these non included edges in the minimal subtour
                minimal_subtour_non_included_edges = list(
                    subtour_non_included_edges)

        return minimal_subtour_non_included_edges

    def find_subtours(self, node_MAP_sol):
        # find all subtours of the MAP optimal solution

        # create a copy of the MAP solution as the solution is used by other
        # methods and passed by reference
        sol = node_MAP_sol.copy()

        # create mapping between consecutive pairs of vertices
        # this will help you follow along each subtour
        consecutive_vertex_mapping = {}
        for out_vertex, in_vertex in node_MAP_sol:
            consecutive_vertex_mapping[out_vertex] = in_vertex

        # get all teh subtours
        subtours = []
        # while there are still subtours
        while sol:
            # get the next subtour
            subtour = []
            # start the next subtour from the first remaining vertex in the
            # MAP solution
            out_vertex, _ = sol[0]
            # initialize a list of vertices already visited in this subtour
            visited_vertices = {out_vertex}
            while True:
                # find the next vertex in the subtour
                in_vertex = consecutive_vertex_mapping[out_vertex]
                # add next edge in  the subtour to the subtour
                subtour.append((out_vertex, in_vertex))
                # remove the edge from the list of edges in the solution
                sol.remove((out_vertex, in_vertex))
                # if we have already visted this in_vertex then we have completed
                # this subtour
                if in_vertex in visited_vertices:
                    subtours.append(subtour)
                    break
                else:
                    # if this in vertex is not yet visited then we haven't completed
                    # the subtour
                    visited_vertices.add(in_vertex)
                    out_vertex = in_vertex

        return subtours

    def prune_queue(self):
        # remove all subproblems from the unpruned subproblems queue
        # whose lower bound is no better than the best cost found so far

        # create a new queue to which we will add all subproblems that can't yet
        # be pruned
        new_queue = queue.PriorityQueue()

        # iterate through the queueand insert all subproblems that can't yet be
        # pruned in the new subproblems queue new_queue. Since the queue is in non
        # decreasing order of lower bounds, there first x subproblems in the queue
        # won't yet be pruneable.
        #  Once you reach the point in the queue where all remaining subproblems have
        # lower bound higher higher than the best determined cost so far, we can
        # just delete the original queue
        while not self.unpruned_nodes.empty():
            lower_bound, node = self.unpruned_nodes.get()

            if lower_bound < self.best_cost:
                new_queue.put((lower_bound, node))

            else:
                self.pruned_subproblems += (self.unpruned_nodes.qsize() + 1)
                break

        self.unpruned_nodes = new_queue
