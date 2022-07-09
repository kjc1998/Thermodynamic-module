import functools
from typing import List, Optional, Union

from solver import expression_solver

from thermodynamics.assumptions import assumptions


@assumptions.ParamDecorators
class IdealGas(assumptions.Assumptions):
    def __init__(
        self,
        callable: Union[assumptions.AbstractDevice, assumptions.Assumptions],
        pressure: Optional[str] = "P",
        volume: Optional[str] = "V",
        mol: Optional[str] = "n",
        gas_constant: Optional[str] = 8.3145,
        temperature: Optional[str] = "T",
    ):
        functools.update_wrapper(self, callable)
        self._callable = callable

        self._equation = expression_solver.EquationFormat(
            LHS=f"{pressure}*{volume}", RHS=f"{mol}*{gas_constant}*{temperature}"
        )

    def __call__(self, *args, **kwargs) -> List[expression_solver.EquationFormat]:
        return self._callable(*args, **kwargs) + [self._equation]
