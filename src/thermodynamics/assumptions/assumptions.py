import abc
import functools
from typing import Callable


def param_decorators(deco: Callable) -> Callable:
    """
    Allowing decorators to take in value arguments
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
