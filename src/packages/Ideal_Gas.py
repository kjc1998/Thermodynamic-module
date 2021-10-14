from . import imports


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
            P, V, T = self.calculate_variable([P, V, T], m=m, R=R)

        # variable setups
        self.pressure = P
        self.volume = V
        self.temperature = T
        self.mass = m
        self.molar = R
        self.density = self.mass / self.volume

        # default to 3 s.f. accurate
        if imports.round_to_sf(P*V, sf) == imports.round_to_sf(m*R*T, sf):
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
