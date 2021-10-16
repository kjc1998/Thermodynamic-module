import math


class OperatorFunction():
    def __init__(self):
        primary_declaration = {
            "+": [self.simple_addition, 0],
            "-": [self.simple_subtraction, 0],
            "*": [self.simple_product, 1],
            "/": [self.simple_division, 1],
            "^": [self.simple_power, 1],
        }
        self.special_to_function = {
            "sin": self.simple_sin,
            "cos": self.simple_cos,
            "tan": self.simple_tan,
            "sqrt": self.simple_sqrt,
            "log10": self.simple_log10,
            "ln": self.simple_ln,
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
