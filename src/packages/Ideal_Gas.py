from .. import imports


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
        if P*V == m*R*T:
            self.pressure = P
            self.volume = V
            self.mass = m
            self.molar = R
            self.temperature = T
        else:
            raise Exception(
                "The coefficients do not match up ideal gas assumption")

    def get_density(self):
        return self.mass / self.volume
