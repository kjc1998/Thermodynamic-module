"""
Necessary Imports File
"""
try:
    from . import general_functions
    from .calculator.math_linear import LinearSolver
except ImportError:
    import general_functions
    from calculator.math_linear import LinearSolver
