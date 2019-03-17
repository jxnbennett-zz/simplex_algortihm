import re
import numpy as np

# Note that throught the code, the 6 programming requirements are indicated by a border made of
# equal signs ('=') and the requirement in all caps followed by the requirement number

class simplex_two_phase:

    # first initialize class with all variables we'll need to implement simplex
    def __init__(self):
        self.c_mat = []
        self.b_mat = []
        self.a_mat = []
        self.prob_type = 'min'
        self.tableau = []
        self.variables = []
        self.basis = []
        self.init_basis = []
        self.num_vars = 0

    # get string input and parse into objective function
    # note all variables must have a coefficient (e.g. 1x1)
    # and negative signs must not be separated by a space from the appropriate coefficient
    # (e.g. -8x1)
    def get_obj_fxn(self, obj_string):
        # first strip input string
        obj_string = obj_string.strip()
        # identify problem type and strip relevant word from string
        if obj_string.startswith('min'):
            self.prob_type = 'min'
            obj_string = obj_string.strip('min')
        elif obj_string.startswith('max'):
            self.prob_type = 'max'
            obj_string = obj_string.strip('max')
        # split string into different terms
        # regex below splits at '+' or '-' (but keeps '-' in the term)
        obj_components = re.split('\+|(-[^\+|-]+)', obj_string)
        for obj_component in obj_components:
            # check to make sure component is a valid term
            if obj_component is not None:
                if len(obj_component) >= 2:
                    # first strip spaces from term
                    obj_component = obj_component.strip()
                    # find term coefficient
                    coef = int(re.findall('^-?[0-9]+', obj_component)[0])
                    # find term variable
                    var = re.findall('[a-zA-Z]+[0-9]+', obj_component)[0]
                    # add variables and coefficients to class
                    self.variables.append(var)
                    self.c_mat.append(coef)
        self.num_vars = len(self.variables)
        # Convert problem to minimization if it's a maximization
        if self.prob_type == 'max':
            self.c_mat = [-1 * coef for coef in self.c_mat]

    # =======================
    # FORM CONVERSION (PR #1)
    # =======================
    # The code below takes a wide variety of equalities (<=, =, >=) and b values (positive or negative)
    # as a string and converts them to the corresponding standard form, adding slack and artifical variables
    # where appropriate. It returns a coefficient, variable, and value matrix used to construct the
    # initial tableau
    def add_constraints(self, const_string):
        # First strip the input string
        const_string = const_string.strip()
        # Split string into the left side (equation), inequality, and right side (value)
        left_side, equality, right_side = re.split('(=|>=|<=)', const_string)
        # If we have equals equality, convert to two constraints: >= and <=
        if equality == '=':
            new_const1 = const_string.replace('=', '>=')
            new_const2 = const_string.replace('=', '<=')
            self.add_constraints(new_const1)
            self.add_constraints(new_const2)
        else:
            b_val = int(right_side.strip())
            # Initialize variable array
            var_coeffs = [0 for i in range(len(self.variables))]
            # Split left equation into its subcomponents
            left_comps = re.split('\+|(-[^\+|-]+)', left_side)
            # Iterate through each component
            for left_comp in left_comps:
                # Make sure each component is valid
                if left_comp is not None:
                    if len(left_comp) >= 2:
                        left_component = left_comp.strip()
                        # Find coefficient associate with component
                        coef = int(re.findall('^-?[0-9]+', left_component)[0])
                        # Find variable name
                        var = re.findall('[a-zA-Z]+[0-9]+', left_component)[0]
                        # Find propoer index of variable name and add it to corresponding index of
                        # coeffcient array
                        var_ind = self.variables.index(var)
                        var_coeffs[var_ind] = coef
            # If b is negative, we have to modify some values
            if b_val < 0:
                # First we'll make all of the variables negative
                var_coeffs = [-1 * coef for coef in var_coeffs]
                # Then we change the value of b itself
                b_val *= -1
                # Next we change the equality type if necessary
                if equality.strip() == '<=':
                    equality = '>='
                elif equality.strip() == '>=':
                    equality = '<='
            # get index of location to insert slack variable
            try:
                slack_insert_ind = self.variables.index('a1')
            except:
                slack_insert_ind = len(self.variables)
            # Check to see if there are any existing slack variables
            prev_var = self.variables[slack_insert_ind - 1]
            # If there are, name the new one appropriately
            if prev_var.startswith('s'):
                slack_ind = int(prev_var[1:])
                new_slack = slack_ind + 1
            # Otherwise the new slack variable is s1
            else:
                new_slack = 1
            # If this isn't an equality, we'll have to actually add a slack variable
            # The first thing we do is insert 0's in the appropriate places in the objective
            # function and coefficient matrix. Then we add the new variable to the variable list
            for array in self.a_mat:
                array.insert(slack_insert_ind, 0)
            self.c_mat.insert(slack_insert_ind, 0)
            self.variables.insert(slack_insert_ind, 's' + str(new_slack))
            # Depending on the equality type, we determing the appropriate coefficient for the slack variable
            if equality.strip() == '<=':
                var_coeffs.insert(slack_insert_ind, 1)
            elif equality.strip() == '>=':
                var_coeffs.insert(slack_insert_ind, -1)
            # If the equality isn't a <=, we'll need to add an artificial variable
            if equality.strip() != '<=':
                # Similar to slack variable procedure; goal is to appropriately name new variable
                last_var = self.variables[-1]
                if last_var.startswith('a'):
                    art_ind = int(last_var[1:])
                    new_art = art_ind + 1
                else:
                    new_art = 1
                # Similar to slacks, we'll add a column of 0's to the tableau
                for array in self.a_mat:
                    array.append(0)
                self.c_mat.append(0)
                self.variables.append('a' + str(new_art))
                var_coeffs.append(1)
            # Finally we append the new values to the exisiting matrices
            self.a_mat.append(var_coeffs)
            self.b_mat.append(b_val)

    # Code to initialize tableau if two phase approach isn't required
    def init_tableau(self):
        # Initialize a tableau of the appropriate size
        tab_init = np.zeros([len(self.a_mat) + 1, len(self.c_mat) + 1])
        # Set values
        tab_init[0, :-1] = np.array(self.c_mat) * -1
        tab_init[1:, :-1] = self.a_mat
        tab_init[1:, -1] = self.b_mat
        first_slack = self.variables.index('s1')
        self.basis = self.variables[first_slack:].copy()
        self.init_basis = self.basis.copy()
        return tab_init

    # Intialize phase 1 tableau
    def init_phase1(self):
        # First we set a preliminary tableau just from the coefficient matrix
        prelim_tableau = np.array(self.a_mat)
        # Next we'll find out the basis in the correct order
        self.basis = ['' for i in range(prelim_tableau.shape[0])]
        # cb_init is the initial cost coefficients for the phase 1 problem
        cb_init = np.zeros(prelim_tableau.shape[0])
        # The final_mult vector is made of 1's and 0's to make sure reduced costs are correct at the end
        final_mult = np.ones(prelim_tableau.shape[1] + 1)
        # Iterate through each column associated with a slack or artifical variable
        for col_ind in range(prelim_tableau[:, self.num_vars:].shape[1]):
            # Set appropriate index and get corresponding column
            cur_col_ind = self.num_vars + col_ind
            cur_col = prelim_tableau[:, cur_col_ind]
            # There are only two possible sums: 1 and -1. If the sum is 1, the column will be used in the
            # initial basis
            if cur_col.sum() == 1:
                # get location of 1 to determine where in the basis the corresponding variable belongs
                cb_to_put = np.argwhere(cur_col == 1).flatten()[0]
                self.basis[cb_to_put] = self.variables[cur_col_ind]
                # set final_mult to 0 to ensure reduced cost is 0
                final_mult[cur_col_ind] = 0
                # the objective function is the sum of articial variables, so if the variable is an
                # articifical one, we add a variable to the cost coefficients in the appropriate spot
                if self.variables[cur_col_ind].startswith('a'):
                    cb_init[cb_to_put] = 1
        # Make a copy of the initial basis to use for future calculations
        self.init_basis = self.basis.copy()
        # Initialize full tableau and set appropriate values
        full_tableau = np.zeros([len(self.a_mat) + 1, len(self.c_mat) + 1])
        full_tableau[1:, :-1] = self.a_mat
        full_tableau[1:, -1] = self.b_mat
        # Calculate reduced costs
        full_tableau[0, :] = np.dot(cb_init, full_tableau[1:, :])
        # Set reduced costs to 0 if necessary
        full_tableau[0, :] = np.multiply(full_tableau[0, :], final_mult.T)
        return full_tableau

    def init_phase2(self):
        # This code is to find b_inverse and the appropriate cb if desired (not necessary)
        #         b_inv = np.zeros([self.tableau.shape[0]-1, self.tableau.shape[0] - 1])
        #         cb_phase2 = np.zeros(self.tableau.shape[0]-1)
        #         inv_col_ind = 0
        #         for var in self.init_basis:
        #             var_ind = self.variables.index(var)
        #             b_inv[:, inv_col_ind] = self.tableau[1:, var_ind]
        #             inv_col_ind += 1

        #         cb_col_ind = 0
        #         for var in self.basis:
        #             var_ind = self.variables.index(var)
        #             cb_phase2[cb_col_ind] = self.c_mat[var_ind]
        #             cb_col_ind += 1

        #         cb_b_inv = np.dot(cb_phase2, b_inv)

        # Find the index of the first articifical variable to know where to terminate tableau
        # Note this is guaranteed to exist if we do a two-phase implementation
        art_ind = self.variables.index('a1')
        # Initialize a tableau of the correct size
        prelim_tableau = np.zeros(self.tableau[:, :art_ind + 1].shape)
        # Set appropriate values and remove artificial variables from tableau
        prelim_tableau[:, :-1] = self.tableau[:, :art_ind]
        prelim_tableau[:, -1] = self.tableau[:, -1]
        self.tableau = prelim_tableau.copy()
        # Add correct reduced costs for phase 2
        self.tableau[0, :] = np.array(self.c_mat[:art_ind + 1]) * -1
        row_ind = 1
        # Make reduced costs 0 for all variables in the basis
        for var in self.basis:
            var_ind = self.variables.index(var)
            self.tableau[0, :] -= self.tableau[row_ind, :] * self.tableau[0, var_ind]
            row_ind += 1

    def pivot(self, enter_ind, leave_ind):
        # Leaving index is one high; correct for that
        # update basis to reflect new variable
        self.basis[leave_ind - 1] = self.variables[enter_ind]
        # Divide row to get a value of 1 for the new basic variable
        self.tableau[leave_ind, :] /= self.tableau[leave_ind, enter_ind]
        # Make all other variables 0 in column
        for row_ind in [i for i in range(self.tableau.shape[0]) if i != leave_ind]:
            factor = self.tableau[row_ind, enter_ind]
            self.tableau[row_ind, :] -= factor * self.tableau[leave_ind, :]

    def ratio_test(self):
        # start by implementing Dantzig's rule
        # get the index of the most positive reduced cost
        enter_ind = np.argmax(self.tableau[0, :-1])
        ratios = []
        # calculate relevant ratios for max reduced cost
        for i in range(self.tableau[1:, :].shape[0]):
            # make sure that y_i is positive
            if self.tableau[i + 1, enter_ind] > 0:
                ratios.append(self.tableau[i + 1, -1] / self.tableau[i + 1, enter_ind])
            # if not positive, set ratio as infinity to preserve index order
            else:
                ratios.append(np.inf)
        ratios = np.array(ratios)
        # get array of indices where ratio is the minimum ratio
        min_indices = np.argwhere(ratios == np.min(ratios)).flatten().tolist()
        # ============================
        # UNBOUNDEDNESS CHECK (PR #6a)
        # ============================
        # During the preceeding ratio test, ratios are recorded as infinity if the corresponding
        # y_i value is non-positive. If all ratios are infinity, that implies there are no positive
        # y_i values and the problem is unbounded
        if ratios.min() == np.inf:
            print('This problem is unbounded, algorithm terminating')
            return -1, -1
        # if there is only one minimum, proceed as normal
        if len(min_indices) == 1:
            leave_ind = np.argmin(ratios) + 1
        # else implement Bland's rule to prevent cycling

        # =========================
        # ANTI-CYCLING RULE (PR #5)
        # =========================
        else:
            # get index of first postive reduced cost
            enter_ind_cands = np.argwhere(self.tableau[0, :-1] > 0).flatten().tolist()
            enter_ind = enter_ind_cands[0]
            # get index of first positive y_i
            pos_ratios = np.argwhere(self.tableau[1:, enter_ind] > 0).flatten().tolist()
            leave_ind = pos_ratios[0] + 1
        return enter_ind, leave_ind

    def dual_test(self):
        leave_ind = np.argmin(self.tableau[1:, -1]) + 1
        ratios = []
        for i in range(self.tableau[:, :-1].shape[1]):
            # make sure that y_i is negative
            if self.tableau[leave_ind, i] < 0:
                ratios.append(self.tableau[0, i] / self.tableau[leave_ind, i])
            # if not positive, set ratio as infinity to preserve index order
            else:
                ratios.append(np.inf)
        enter_ind = np.argmin(ratios)
        print(min(ratios))
        return enter_ind, leave_ind

    def phase_one(self):
        # Initialize tableau using phase one formulation
        self.tableau = self.init_phase1()
        # Set enter and leaving indices to prevent code crashing in event table is already at optimum
        ent, lev = (0, 0)
        # While there is a single positive reduced cost, pivot the table and look for optimal solution

        while not np.all(self.tableau[0, :-1] <= 0) or not np.all(self.tableau[1:, -1] >= 0):
            if not np.all(self.tableau[1:, -1] >= 0):
                ent, lev = self.dual_test()
            else:
                ent, lev = self.ratio_test()
            if ent == -1:
                return 0
            self.pivot(ent, lev)

        # Display phase 1 tableau
        print('Phase 1 final tableau:')
        # Check to see if the objective value is 0
        if abs(self.tableau[0, -1]) <= 1e-5:
            # Determine whether or not there are artificial variables left in the basis
            # This can happen if the initial equality had a right hand value of 0
            art_list = [1 if var.startswith('a') else 0 for var in self.basis]

            # If this is the case, replace the artificial variables in the basis with the slack variable
            # from the same constraint
            non_basic = list(set(self.variables) - set(self.basis))
            for index in range(len(art_list)):
                if art_list[index] == 1:
                    lev = index + 1
                    candidates = [i for i in range(self.tableau[:, self.num_vars:].shape[1]) if
                                  self.tableau[lev, i + self.num_vars] != 0]
                    ent = candidates[0] + self.num_vars
                    self.pivot(ent, lev)

            # =============================
            # REDUNDANT ROW REMOVAL (PR #3)
            # =============================
            # If in the final phase 1 tableau there is a row where all of the non-artificial variables
            # are 0, that implies the row is redundant and can be removed. Note that slack variables
            # must also be 0 as they indicate the type of equality.
            # e.g. x1+x2 <= 3 and x1+x2 >= 3 are cleary not redundant constraints (they're actually an equality)
            # The code below checks that conditions and removes variables as appropriate
            last_rel_var = self.variables.index('a1')
            cols_to_check = [i for i in range(last_rel_var)]
            cols_to_check.append(-1)
            to_delete = []
            basis_to_rem = []

            for row in range(self.tableau.shape[0] - 1):
                # Check to see if all appropriate values are 0
                if np.all(self.tableau[row + 1, cols_to_check] == 0):
                    # If they are, plan to delete the row and remove the related variable from the basis
                    to_delete.append(row + 1)
                    basis_to_rem.append(self.basis[row])
                    print('deleted row ', row + 1, 'as it is redundant')
            # Carry out deletions
            self.tableau = np.delete(self.tableau, to_delete, axis=0)
            self.basis = [variable for variable in self.basis if variable not in basis_to_rem]

            # Print that we are proceeding to phase 2
            print('\nOptimal phase 1 solution acheived...\nproceeding to phase 2')

            return 1
        # =========================
        # FEASIBILITY CHECK (PR #2)
        # =========================
        # If phase 1 arrives at a solution where the optimal value is something other than 0
        # then the original problem is infeasibility. Print that information to screen
        else:
            print('The optimal value for phase 1 is non-zero\nThis problem is infeasible')
            return 0

    def phase_two(self):
        # Initialize phase two
        self.init_phase2()

        # Set enter and leaving indicies to prevent future crash in event table is already at optimum
        ent, lev = (0, 0)
        # =========================
        # OPTIMAL SOLUTION (PR #6b)
        # =========================
        # After each pivot, the algorithm checks to see if there are any positive reduced costs
        # If there are, it continues the algorithm, but if not it terminates and informs the user
        # Whether an optimal solution has been found or if the problem is unbounded
        # Note that this requirement is present in phase one and normal tableau implementations,
        # but highlighted here as it will be the most common implementationprint()
        while not np.all(self.tableau[0, :-1] <= 0) or not np.all(self.tableau[1:, -1] >= 0):
            if not np.all(self.tableau[1:, -1] >= 0):
                ent, lev = self.dual_test()
                print(ent, lev)
            else:
                ent, lev = self.ratio_test()
            if ent == -1:
                return 0
            self.pivot(ent, lev)

        # If either index is -1, it implies the solution is unbounded
        if ent == -1:
            print('Try changing constraints')
        # If algorithm terminates, print out final solution
        else:
            print('\n=========')
            print('SOLUTION')
            print('=========')
            solution_dict = {}
            for i in range(len(self.basis)):
                if not self.basis[i].startswith('s'):
                    solution_dict[self.basis[i]] = self.tableau[i + 1, -1].round(2)
            print('final_values')
            print(solution_dict)
            if self.prob_type == 'min':
                obj = self.tableau[0, -1]
            else:
                obj = -1 * self.tableau[0, -1]
            print('objective value: ', obj)

    def normal_tableau(self):
        # Intialization for normal approach
        self.tableau = self.init_tableau()
        # While reduced costs are not all non-positive
        while not np.all(self.tableau[0, :-1] <= 1e-5):
            ent, lev = self.ratio_test()
            if ent == -1:
                break
            self.pivot(ent, lev)
        # Check for unboundedness
        if ent == -1:
            print('Try changing constraints')
        # Print out solution
        else:
            print('\nOptimal value achieved;\n Final Tableau:')
            print('\n=========')
            print('SOLUTION')
            print('=========')
            solution_dict = {}
            for i in range(len(self.basis)):
                if not self.basis[i].startswith('s'):
                    solution_dict[self.basis[i]] = self.tableau[i + 1, -1].round(2)
            print('final_values')
            print(solution_dict)
            if self.prob_type == 'min':
                obj = self.tableau[0, -1]
            else:
                obj = -1 * self.tableau[0, -1]
            print('objective value: ', obj)

    # Function to put everything together
    def simplex(self):
        # ==============================
        # SIMPLEX INITIALIZATION (PR #4)
        # ==============================
        # Check if any artificial variables were added during problem setup
        # If so, that implies a BFS was not easily available and we should use two-phase implementation
        # If not, there is a BFS easily available from the slack variables (implying all constraints were <=) adnasndalinsdlasd
        last_var = self.variables[-1]
        if last_var.startswith('a'):
            # Start with phase one
            continue_simplex = self.phase_one()
            # If successful, it will return a 1, indicating that we should continue to phase 2
            # Otherwise, the problem is infeasible and the program will state as much
            if continue_simplex:
                self.phase_two()
            else:
                print('Try changing constraints')
        # Otherwise we run the normal implementation
        else:
            self.normal_tableau()
