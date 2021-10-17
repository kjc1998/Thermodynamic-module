from .operations import imports


class IdealGas():
    """
    Variables:      Arguments:      Call:        Units:

    Pressure        P               pressure     Pa
    Volume          V               volume       m3
    Temperature     T               temperature  K
    Mass            m               mass         kg | kgs-1
    Molar Gas       R = 8.3145      molar        J K-1 mol-1
    Density         -               density      kg m-3
    Sig. Figures    sf = 3          -            -
    """

    # default to unit mass unless specified
    def __init__(self, P=None, V=None, T=None, m=1, R=8.3125, sf=3):

        # check missing variable
        if [P, V, T].count(None) > 1:
            raise Exception("Too many unknown variables.")
        elif None in [P, V, T]:
            solver_instance = imports.LinearSolver(
                "P*V=m*R*T", P=P, V=V, m=m, R=R, T=T)

            # lower case
            self.pressure = solver_instance.answer_dict["p"]
            self.volume = solver_instance.answer_dict["v"]
            self.temperature = solver_instance.answer_dict["t"]
            self.mass = solver_instance.answer_dict["m"]
            self.molar = solver_instance.answer_dict["r"]
        else:
            self.pressure = P
            self.volume = V
            self.temperature = T
            self.mass = m
            self.molar = R
        self.density = self.mass / self.volume

        # default to 3 s.f. accurate
        if imports.general_functions.round_to_sf(self.pressure*self.volume, sf) == imports.general_functions.round_to_sf(self.mass*self.molar*self.temperature, sf):
            pass
        else:
            raise Exception(
                "The coefficients do not match up ideal gas assumption.")

    def calculate_variable(self, variable_list, m=1, R=8.3125):
        ans = variable_list
        if not variable_list[0]:
            ans[0] = ans[2]*m*R/ans[1]
        elif not variable_list[1]:
            ans[1] = ans[2]*m*R/ans[0]
        else:
            ans[2] = ans[0]*ans[1]/(m*R)
        return ans
