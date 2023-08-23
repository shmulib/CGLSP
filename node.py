from MAP_solver import google_or_AP_solver
import numpy as np
import time
from timeout_decorator import timeout


class Node:
    def __init__(
        self,
        cost_matrix,
        instance_size,
        included_edges,
        excluded_edges,
        lower_bound,
    ):
        self.cost_matrix = cost_matrix
        self.instance_size = instance_size
        self.included_edges = included_edges
        self.excluded_edges = excluded_edges
        self.subproblem_cost_matrix = self.create_subproblem_cost_matrix(
            cost_matrix, included_edges, excluded_edges
        )
        self.lower_bound = lower_bound
        # store creation time of Node - it will be used to break ties on Node
        # with same priority in the BnB unpruned_nodes queue
        self.creation_time = time.time()

    # define custom comparison for Nodes based on creation time
    def __lt__(self, other):
        # Compare based on creation time (timestamp)
        return self.creation_time < other.creation_time

    def __eq__(self, other):
        # Compare based on creation time (timestamp)
        return self.creation_time == other.creation_time

    def create_subproblem_cost_matrix(
        self, cost_matrix, included_edges, excluded_edges
    ):
        """
        The cost matrix required for the subproblem has to be modified
        to reflect the fixed edges (included and excluded) in the subproblem

        By can exclude all edges in the subproblem cost matrix columns containing the
        included edges, except the included edges, thus preventing them from being 
        selected in the MAP solution for the subproblem, hence achieveing the 
        objective of having only the included edges selected

        All excluded edges simply have their edge cost set to "NA" so that they
        won't be selected
        """
        subproblem_cost_matrix = cost_matrix.copy()

        if included_edges:

            # for each already included edge (i,j) that is fixed for this subproblem
            # the subproblem cost matrix assigns "NA"
            # to to all edges (i,k) k!=j

            # get included edge row and col indices in lists for indexing purposes
            (
                included_edges_row_indices,
                included_edges_col_indices
            ) = self.get_edge_indices(included_edges)

            # for each col that an included edge is in, set all values in that
            # col to "NA", including included edge
            # we will restore the included edges to their original cost
            col_mask = np.zeros(cost_matrix.shape[0], dtype=bool)
            col_mask[included_edges_col_indices] = True
            subproblem_cost_matrix[:, col_mask] = "NA"

            # restore actual cost for included edges
            included_edges_costs = cost_matrix[included_edges_row_indices,
                                               included_edges_col_indices]
            subproblem_cost_matrix[included_edges_row_indices,
                                   included_edges_col_indices] = included_edges_costs

        # set the sub_problem_cost_matrix entries for excluded edges to "NA" as
        # they can't be selected for this subproblem
        if excluded_edges:
            (
                excluded_edges_row_indices,
                excluded_edges_col_indices,
            ) = self.get_edge_indices(excluded_edges)

            subproblem_cost_matrix[
                excluded_edges_row_indices, excluded_edges_col_indices
            ] = "NA"

        return subproblem_cost_matrix

    def solve_MAP(self):
        # Solve the Modified Assignment Problem for this subproblem

        # Use Google OR-Tools AP Solver to find MAP relaxation solution
        # for this subproblem
        # The optimal edges determined by the solver will only include
        # those not already fixed in this subproblem
        (
            self.MAP_solution,
            self.MAP_min_cost,
            MAP_partial_assignment_costs,
            self.MAP_solve_status,
        ) = google_or_AP_solver(self.subproblem_cost_matrix)

        # if the solution status is infeasible, then subproblem doesn't have an
        # MAP feasible solution, so we can prune this node from the branch and bound
        # tree
        # if the subproblem is the whole problem i.e. root node, then the CGLSP
        # has no feasible solutions
        if self.MAP_solve_status == "INFEASIBLE":
            return

        # otherwise,the solver may have failed to solve because of
        # an integer overflow error
        elif self.MAP_solve_status == "POSSIBLE_OVERFLOW":
            return

        # otherwise the Google AP solver found the optimal solution to the MAP
        # for this subproblem

        # if the optimal cost for the MAP for this subproblem which is a
        # lower bound for this subproblem is tighter than previously
        # obtained lower bound, then we need to update the best lower bound
        if self.MAP_min_cost > self.lower_bound:
            self.lower_bound = self.MAP_min_cost

        return

    def MAP_sol_CGLSP_feasible(self):
        # note if lower bound obtained using cost reduction is higher
        # then MAP_min_cost, then the MAP solution can't be feasible for CGSLP
        # because that would imply there is a feasible solution better than an
        # established lower bound, so we don't need to check if there are subtours in
        # the MAP, we already know there must be

        # MAP solution is feasible for CGLSP if it the edges form one tour, i.e. a
        # hamiltonian circuit has been found otherwise MAP contains subtours

        edge_dict = {}
        for first_job, second_job in self.MAP_solution:
            edge_dict[first_job] = second_job

        # starting at job 0, follow the edges through the graph until you have visited
        # enough jobs to complete a hamiltonian circuit, if no nodes are visited twice
        # in this sequence, then a hamaltonian circuit exists in this solution
        # otherwise this MAP contains subtours

        cur_job = 0
        path_length = 0
        tour_length = len(self.MAP_solution)  # 5
        visited_jobs = set()
        while path_length < tour_length:
            next_job = edge_dict[cur_job]

            if next_job in visited_jobs:
                return False
            else:
                visited_jobs.add(next_job)
                path_length += 1
                cur_job = next_job

        return True

    def get_cost_reduction_lower_bound(self):
        # First LB procedure for subproblem using cost matrix reduction
        # if the lower bound obtained using cost matrix reduction
        # is higher than the lower bound inherited from the node's parent
        # then we update the lower bound for this subproblem

        # PLACEHOLDER
        cost_reduction_LB = -1

        if cost_reduction_LB > self.lower_bound:
            self.lower_bound = cost_reduction_LB

        return

    def get_feasible_sol(self):

        # heuristic solve to generate feasible sol to subproblem
        # used to generate initial solution for root problem

        # PLACEHOLDER heuristic solution using the fact that the sequence of jobs
        # [0,1,...instance_size-1] is a feasible solution of the CGSLP instances
        n = self.instance_size
        solution = [(i, (i+1) % n) for i in range(n)]
        row_indices, col_indices = self.get_edge_indices(solution)
        cost = self.cost_matrix[row_indices, col_indices].sum()

        # PLACEHOLDER NO FEASIBLE SOLUTIONS
        # solution = []
        # cost = -1

        return cost, solution

    def get_edge_indices(self, edge_list):
        # utility function
        # converts list of edges into edge row and col indices suitable for indexing a
        # 2d numpy array, i.e. a cost matrix

        edges_row_indices = []
        edges_col_indices = []

        if edge_list:
            edges_row_indices = [edge[0] for edge in edge_list]
            edges_col_indices = [edge[1] for edge in edge_list]

        return edges_row_indices, edges_col_indices
