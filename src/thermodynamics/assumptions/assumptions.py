import abc
import functools
from typing import Callable


class Assumptions(abc.ABC):
    """
    Decorators that can append equations
    """

    @abc.abstractmethod
    def __init__(self, func):
        pass

    @abc.abstractmethod
    def __call__(self) -> Callable:
        pass


class ParamDecorators:
    """
    Allowing decorators to take in value arguments
    """

    def __init__(self, deco: "Assumptions"):
        functools.update_wrapper(self, deco)
        self._deco = deco

    def __call__(self, *args, **kwargs) -> Callable:
        if len(args) != 0 and callable(args[0]):
            return self._deco(args[0])
        return lambda func: self._deco(func, *args, **kwargs)
