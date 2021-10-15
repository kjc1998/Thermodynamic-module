import re
from queue import PriorityQueue
from math_operators import OperatorFunction


class MathSolver():
    ### STANDARD ###
    primary_priority = {"+": 0, "-": 0, "*": 1, "/": 1, "^": 1}
    secondary_priority = {"(": 2, ")": 2}
    ### SPEICAL ###
    special_operator = ["cos", "sin", "tan",
                        "sqrt", "log10", "ln"]
    special_constants = ["pi", "exp"]
    indicator = ["#", "="]

    def __init__(self, string_equation: str, **defined_var_dict):
        self.main_string = string_equation
        self.math_operator = OperatorFunction()
        self.defined_var_dict = defined_var_dict

    def linear_solver(self):
        """
        Function for resolving one unknown variable from equation
        Rules:
            Unknown variable must only appear once in the equation
            i.e. "x + x = 1" is not allowed
        Example:
            string = "(x + 2) / y = ( z + 1 )^-1"
            variable = {x = 1, y = 2}
            Automatically detect unkown z variable and solve it
        """
        string_equation = self.string_trimming(self.main_string)

        ### CHECK VALID ###
        check_list = list(
            {**self.primary_priority, **self.secondary_priority}.keys()) + self.special_operator + self.special_constants + self.indicator
        index_var_dict = self.find_variables(
            string_equation, check_list)
        if not self.is_valid_equation(string_equation, index_var_dict):
            raise Exception("Not enough arguments to resolve equation")

        ### BRACKETS PRIORITY ###

    def simple_solver(self, sub_string: str):
        """
        Recursive function for solving simple equation expressions (substituted)
        i.e. -2+3/2*3 returns 2.5
        """
        # trimming string
        sub_string = self.string_trimming(sub_string)
        try:
            ans = float(sub_string[:-1])
            return ans
        except ValueError:
            value, operation, target = "", "", ""
            swap = False
            operation_system = PriorityQueue()
            for index in range(len(sub_string)):
                character = sub_string[index]
                if character == "#":
                    operation_system.put((-1*self.primary_priority[operation], [
                        value, operation, target]))
                elif character not in self.primary_priority.keys():
                    if swap:
                        target += character
                    else:
                        value += character
                else:
                    if value and not target:
                        operation = character
                        swap = True
                    elif value and target:
                        operation_system.put((-1*self.primary_priority[operation], [
                            value, operation, target]))
                        value = target
                        operation = character
                        target = ""
                    else:
                        value += character  # + - sign
            value, operation, target = operation_system.get()[1]
            operator_function = self.math_operator.sign_to_function[operation]
            current_ans = operator_function(value, target)
            final_string = sub_string.replace(
                f"{value}{operation}{target}", str(current_ans))
            return self.simple_solver(final_string)

    def string_trimming(self, string_equation):
        """
        Process equation expressions
        """
        string_equation = string_equation.lower()
        string_equation = string_equation.replace(" ", "")
        string_equation = string_equation.replace("#", "")
        string_equation = string_equation.replace("**", "^")
        string_equation = re.sub(r"\{|\[", "(", string_equation)
        string_equation = re.sub(r"\}|\]", ")", string_equation)
        special_dict = {
            r"log10\(|lg10\(": "log10(",
            r"loge\(|ln\(|log\(": "ln(",
        }
        for special_key in list(special_dict.keys()):
            string_equation = re.sub(
                special_key, special_dict[special_key], string_equation)
        return string_equation + "#"

    def find_variables(self, string_equation: str, check_list: list):
        # trimming string
        string_equation = self.string_trimming(string_equation)
        index_var_dict, variable_string = {}, ""
        for character_index in range(len(string_equation)):
            character = string_equation[character_index]
            if character not in check_list:
                variable_string += character
            else:
                if variable_string and variable_string not in check_list:
                    start_index = character_index - len(variable_string)
                    index_var_dict[start_index] = variable_string
                variable_string = ""
        return index_var_dict

    def is_valid_equation(self, string_equation: str, index_var_dict: dict):
        # trimming string
        string_equation = self.string_trimming(string_equation)
        valid_counter = 0
        for index in list(index_var_dict.keys()):
            try:
                float(index_var_dict[index])
            except ValueError:
                valid_counter += 1
        if "=" in string_equation:
            # always one argument short
            if valid_counter != len(self.defined_var_dict)+1:
                return False
        else:
            # equals argument number
            if valid_counter != len(self.defined_var_dict):
                return False
        return True


test = MathSolver("-2+3/2*3^2# + log{{[a]}} = cos(2)")
test.linear_solver()
ans = test.simple_solver(test.string_trimming("+3"))
print(ans)
