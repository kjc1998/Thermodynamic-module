import math


class OperatorFunction():
    def __init__(self):
        self.sign_to_function = {
            "*": self.simple_product,
            "/": self.simple_division,
            "^": self.simple_power,
            "+": self.simple_addition,
            "-": self.simple_subtraction,
            "sin": self.simple_sin,
            "cos": self.simple_cos,
            "tan": self.simple_tan,
            "sqrt": self.simple_sqrt,
            "log10": self.simple_log10,
            "ln": self.simple_ln,
        }

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

    def simple_sqrt(target):
        return math.sqrt(float(target))

    def simple_log10(target):
        return math.log10(float(target))

    def simple_ln(target):
        return math.log(float(target))
