import re
import math
import time
from queue import PriorityQueue
from math_operators import OperatorFunction


class MathSolver():
    ### STANDARD ###
    primary_priority = {"+": 0, "-": 0, "*": 1, "/": 1, "^": 1}
    secondary_priority = {"(": 1, ")": -1}
    ### SPEICAL ###
    special_operator = ["cos", "sin", "tan",
                        "sqrt", "log10", "ln"]
    special_constants = {"pi": math.pi, "exp": math.e}
    indicator = ["#", "="]

    def __init__(self, string_equation: str, **defined_var_dict: dict):
        self.math_operator = OperatorFunction()
        self.main_string = string_equation
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

        ### VALID EQUATION ###
        check_list = list(
            {**self.primary_priority, **self.secondary_priority, **self.special_constants}.keys()) + self.special_operator + self.indicator
        index_var_dict = self.find_variables(
            string_equation, check_list)
        if not self.is_valid_equation(string_equation, index_var_dict):
            raise Exception("Not enough arguments to resolve equation.")
        if string_equation.count("(") != string_equation.count(")"):
            raise Exception("Number of brackets do not match.")
        ### SUB VARIABLES ###
        offset = 0
        for index in list(index_var_dict.keys()):
            variable = index_var_dict[index]
            try:
                new_index = index-offset
                sub_value = str(self.defined_var_dict[variable])
                offset += len(variable)-len(sub_value)
                string_equation = string_equation[:new_index] + \
                    sub_value + string_equation[new_index+len(variable):]
            except KeyError:
                pass
        ### SUB SPECIAL CONSTANT ###
        for special_constant in list(self.special_constants.keys()):
            string_equation = string_equation.replace(
                special_constant, str(self.special_constants[special_constant]))
        ### BRACKETS PRIORITY ###
        sub_index_dict = self.set_priority(string_equation)
        substituted_dict = self.substitute_value(
            string_equation, sub_index_dict)
        for initial, sub in substituted_dict.items():
            string_equation = string_equation.replace(initial, sub)
        ### REDUCED EQUATION ###
        try:
            solve_special = self.get_special({}, string_equation[:-1])[1]
            final_ans = float(self.simple_solver(solve_special))
        except:
            # there exists one unknown within the formula
            reduced_equation = string_equation[:-1]
            left_hand, right_hand = reduced_equation.split("=")
            # resolve any lower level special operator
            left_hand = self.simple_solver(
                self.get_special({}, left_hand)[1])
            right_hand = self.simple_solver(
                self.get_special({}, right_hand)[1])
            final_ans = self.twin_solver(left_hand, right_hand)
        return final_ans

    def simple_solver(self, sub_string: str):
        sub_string = self.basic_solver(sub_string)
        sub_string = self.resolve_low_prior(sub_string)
        return sub_string

    def basic_solver(self, sub_string: str):
        """
        Recursive function for solving simple equation expressions (substituted)
        i.e. -2+3/2*3 returns 2.5
        """
        # trimming string
        sub_string = self.string_trimming(sub_string)
        try:
            ans = float(sub_string[:-1])
            return str(ans)
        except ValueError:
            try:
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
                        if value and not target and not operation:
                            operation = character
                            swap = True
                        elif value and target:
                            operation_system.put((-1*self.primary_priority[operation], [
                                value, operation, target]))
                            value = target
                            operation = character
                            target = ""
                        else:
                            # + - sign in front
                            if swap:
                                target += character
                            else:
                                value += character
                value, operation, target = operation_system.get()[1]
                operator_function = self.math_operator.sign_to_function[operation]
                current_ans = operator_function(value, target)
                final_string = sub_string.replace(
                    f"{value}{operation}{target}", str(current_ans))
                return self.simple_solver(final_string)
            except:
                # Accept any kind of error
                return f"({sub_string[:-1]})"

    def resolve_low_prior(self, string_equation):
        string_function = string_equation.lstrip("(").rstrip(")")
        low_prior_value = min(list(self.primary_priority.values()))
        for key, item in self.primary_priority.items():
            if item != low_prior_value:
                continue
            string_split = string_function.split(key)
            base = ""
            for string in string_split:
                current_string = base + string
                current_ans = self.basic_solver(current_string)
                if current_ans[0] == "(" and current_ans[-1] == ")":
                    if base:
                        base = base.rstrip(key)
                        string_equation = string_equation.replace(
                            base, stored_ans)
                        base = ""
                else:
                    stored_ans = current_ans
                    base += string + key
            if base and stored_ans:
                string_equation = string_equation.replace(
                    base.rstrip(key), stored_ans)
        return string_equation

    def string_trimming(self, string_equation: str):
        """
        Process equation expressions
        """
        string_equation = string_equation.lower()
        string_equation = string_equation.replace(" ", "")
        string_equation = string_equation.replace("#", "")
        string_equation = string_equation.replace("**", "^")
        string_equation = re.sub(r"\-\+|\+\-", "-", string_equation)
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

    def set_priority(self, string_equation):
        sub_index_dict = {}
        priority = 0
        for index in range(len(string_equation)):
            character = string_equation[index]
            if character in self.secondary_priority.keys():
                if character == "(":
                    priority += self.secondary_priority[character]
                try:
                    sub_index_dict[priority].append(index)
                except KeyError:
                    sub_index_dict[priority] = [index]
                if character == ")":
                    priority += self.secondary_priority[character]
        return sub_index_dict

    def get_special(self, substituted_dict, sub_expression):
        # variable will not be processed due to no bracket regex rule
        primary_regex = "\)|\(|$|"
        for primary_operator in self.primary_priority:
            primary_regex += f"\{primary_operator}|"
        primary_regex = primary_regex[:-1]
        for special_operator in self.special_operator:
            if re.search(f"{special_operator}[0-9]", sub_expression):
                filter_regex = f"{special_operator}(.*?)({primary_regex})"
                filter_regex = re.compile(filter_regex)
                for match in re.findall(filter_regex, sub_expression):
                    if match[0]:
                        special_function = self.math_operator.sign_to_function[special_operator]
                        special_ans = str(special_function(match[0]))
                        substituted_dict[special_operator +
                                         match[0]] = special_ans
                        sub_expression = sub_expression.replace(special_operator +
                                                                match[0], special_ans)
        return substituted_dict, sub_expression

    def substitute_value(self, string_equation, sub_index_dict):
        # regex catching
        substituted_dict = {}
        for _, value in sorted(sub_index_dict.items(), reverse=True):
            pairs = [value[2*ind:2*ind+2] for ind in range(int(len(value)/2))]
            for pair in pairs:
                sub_expression = string_equation[pair[0]:pair[1]+1]
                for key_sub, value_sub in substituted_dict.items():
                    sub_expression = sub_expression.replace(
                        key_sub, value_sub)
                substituted_dict, sub_expression = self.get_special(
                    substituted_dict, sub_expression)
                substituted = self.simple_solver(sub_expression[1:-1])
                substituted_dict[sub_expression] = substituted
        return substituted_dict

    def twin_solver(self, left_hand, right_hand):
        left_hand = left_hand.rstrip(")").lstrip("(")
        right_hand = right_hand.rstrip(")").lstrip("(")
        return None


test = MathSolver(
    "56/23*2+1+2+22*[exp^P1+123/23 + 9*3]-exp^(9) = 3*2+1")
answer = test.linear_solver()
