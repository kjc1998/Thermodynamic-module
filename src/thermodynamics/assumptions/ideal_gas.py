import functools
from typing import Callable, Optional

from solver import expression_solver

from thermodynamics.assumptions import assumptions


@assumptions.ParamDecorators
class IdealGas(assumptions.Assumptions):
    def __init__(
        self,
        func: Callable,
        pressure: Optional[str] = "P",
        volume: Optional[str] = "V",
        mol: Optional[str] = "n",
        gas_constant: Optional[str] = 8.3145,
        temperature: Optional[str] = "T",
    ):
        functools.update_wrapper(self, func)
        self._func = func

        self._equation = expression_solver.EquationFormat(
            LHS=f"{pressure}*{volume}", RHS=f"{mol}*{gas_constant}*{temperature}"
        )

    def __call__(self, *args, **kwargs) -> Callable:
        return self._func(*args, **kwargs) + [self._equation]
