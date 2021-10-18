import math
import numpy as np


class OperatorFunction():
    def __init__(self):
        primary_declaration = {
            "+": [self.simple_addition, 0],
            "-": [self.simple_subtraction, 0],
            "*": [self.simple_product, 1],
            "/": [self.simple_division, 1],
            "^": [self.simple_power, 2]
        }
        self.special_to_function = {
            "sin": self.simple_sin,
            "cos": self.simple_cos,
            "tan": self.simple_tan,
            "sqrt": self.simple_sqrt,
            "log10": self.simple_log10,
            "ln": self.simple_ln,
            "asin": self.inverse_sin,
            "acos": self.inverse_cos,
            "atan": self.inverse_tan,
        }
        ### STANDARD ###
        self.primary_to_function = {k: v[0]
                                    for k, v in primary_declaration.items()}
        self.primary_priority = {k: v[1]
                                 for k, v in primary_declaration.items()}
        self.secondary_priority = {"(": 1, ")": -1}

        ### SPEICAL ###
        self.special_operator = list(self.special_to_function.keys())
        self.special_constants = {"pi": math.pi, "exp": math.e}

        ### INVERSE ###
        self.inverse_operator = {
            "+": "-",
            "-": "+",
            "*": "/",
            "/": "*",
            # Trigonometry Functions
            "sin": "asin",
            "asin": "sin",
            "cos": "acos",
            "acos": "cos",
            "tan": "atan",
            "atan": "tan",
            "^": "^_target_1/term",  # special primary
            "sqrt": "^_target_2",
            "log10": "^_10_target",
            "ln": "^_exp_target",
        }

    def value_wrapper(self, value):
        return np.format_float_positional(value, trim='-')

    def simple_product(self, ori, target):
        return float(ori)*float(target)

    def simple_addition(self, ori, target):
        return float(ori)+float(target)

    def simple_division(self, ori, target):
        return float(ori)/float(target)

    def simple_subtraction(self, ori, target):
        return float(ori)-float(target)

    def simple_power(self, ori, target):
        return float(ori)**float(target)

    def simple_inverse(self, ori, target):
        return float(ori)**(1/float(target))

    def inverse_log(self, ori, target):
        return math.log10(float(target))/math.log10(float(ori))

    def simple_sin(self, target):
        return math.sin(float(target))

    def simple_cos(self, target):
        return math.cos(float(target))

    def simple_tan(self, target):
        return math.tan(float(target))

    def simple_sqrt(self, target):
        return math.sqrt(float(target))

    def simple_log10(self, target):
        return math.log10(float(target))

    def simple_ln(self, target):
        return math.log(float(target))

    def inverse_sin(self, target):
        return math.asin(float(target))

    def inverse_cos(self, target):
        return math.acos(float(target))

    def inverse_tan(self, target):
        return math.atan(float(target))
