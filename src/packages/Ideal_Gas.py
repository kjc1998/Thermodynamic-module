from . import imports


class IdealGas():
    """
    Variables:      Arguments:

    Pressure        P
    Volume          V
    Temperature     T
    Mass            m
    Molar Gas       R = 8.3145,
    """

    def __init__(self, P, V, T, m, R=8.3125):
        # 3 s.f. accurate
        if imports.round_to_sf(P*V) == imports.round_to_sf(m*R*T):
            self.pressure = P
            self.volume = V
            self.mass = m
            self.molar = R
            self.temperature = T
            self.density = self.mass / self.volume
        else:
            raise Exception(
                "The coefficients do not match up ideal gas assumption")
