import functools
from solver import expression_solver


def param_decorators(deco):
    """
    Allowing decorators to take in arguments
    """

    @functools.wraps(deco)
    def layer(*args, **kwargs):
        if len(args) != 0 and callable(args[0]):
            # calling func directly
            return deco(args[0])
        else:
            # decorators taking in arguments
            return lambda func: deco(func, *args, **kwargs)

    return layer


class Assumptions:
    """
    Decorators that can append equations
    """

    @staticmethod
    @param_decorators
    def ideal_gas(
        func, pressure="P", volume="V", mol="n", gas_constant=8.3145, temperature="T"
    ):
        """
        Function should return a list of EquationFormats
        """
        equation = [
            expression_solver.EquationFormat(
                LHS=f"{pressure}*{volume}", RHS=f"{mol}*{gas_constant}*{temperature}"
            )
        ]

        @functools.wraps(func)
        def inner_wrap(*args, **kwargs):
            return func(*args, **kwargs) + equation

        return inner_wrap
