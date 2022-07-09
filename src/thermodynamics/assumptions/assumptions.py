import abc
from typing import Callable, Union, List, Type
from solver import expression_solver


class AbstractDevice(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> List[expression_solver.EquationFormat]:
        pass


class Assumptions(abc.ABC):
    """
    Decorators that can append list of equations
    Taking in an assumption instance or a device instance which are both callable
    """

    @abc.abstractmethod
    def __init__(self, callable: Union["Assumptions", "AbstractDevice"]):
        pass

    @abc.abstractmethod
    def __call__(self) -> List[expression_solver.EquationFormat]:
        pass


class ParamDecorators:
    """
    Allowing decorators to take in arguments
    If argument consist of callable object, then default to empty argument
    """

    def __init__(self, deco: "Assumptions"):
        self._deco = deco

    def __call__(self, *args, **kwargs) -> Callable:
        def inner_wrap(call: Union["Assumptions", Type["AbstractDevice"]]):
            if isinstance(call, Assumptions):
                return lambda func: self._deco(func, *args, **kwargs)

            return lambda *d_args, **d_kwargs: self._deco(
                call(*d_args, **d_kwargs), *args, **kwargs
            )

        return inner_wrap
