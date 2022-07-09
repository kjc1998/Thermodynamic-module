import abc
import functools
from typing import Callable, Union, List
from solver import expression_solver


class AbstractDevice(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> List[expression_solver.EquationFormat]:
        pass


class Assumptions(abc.ABC):
    """
    Decorators that can append list of equations
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
        functools.update_wrapper(self, deco)
        self._deco = deco

    def __call__(self, *args, **kwargs) -> Callable:
        if len(args) != 0 and callable(args[0]):
            return self._deco(args[0])
        return lambda func: self._deco(func, *args, **kwargs)
