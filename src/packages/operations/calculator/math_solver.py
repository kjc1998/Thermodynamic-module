from math import e
import re
import warnings
import copy
from queue import PriorityQueue
from math_operators import OperatorFunction


class MathSolver(OperatorFunction):
    indicator = ["#", "="]

    def __init__(self, string_equation: str, **defined_var_dict: dict):
        # Operator Function Inheritance
        super().__init__()
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
        string_equation = self.__string_trimming(self.main_string)

        ### VALID EQUATION ###
        check_list = list(
            {**self.primary_priority, **self.secondary_priority, **self.special_constants}.keys()) + self.special_operator + self.indicator
        index_var_dict = self.__variable_search(
            string_equation, check_list)
        unknown_var = self.__is_valid_equation(string_equation, index_var_dict)
        if not unknown_var:
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
        sub_index_dict = self.__set_priority(string_equation)
        orig_sub_dict = self.__variable_substitution(
            string_equation, sub_index_dict)
        for initial, sub in orig_sub_dict.items():
            string_equation = string_equation.replace(initial, sub)
        ### REDUCED EQUATION ###
        try:
            solve_special = self.__special_operator_value(
                {}, string_equation[:-1])[1]
            final_ans = float(self.simple_solver(solve_special))
        except:
            # One Unresolved Unknown
            reduced_equation = string_equation[:-1]
            left_hand, right_hand = reduced_equation.split("=")
            left_hand = self.simple_solver(
                self.__special_operator_value({}, left_hand)[1])
            right_hand = self.simple_solver(
                self.__special_operator_value({}, right_hand)[1])
            final_ans = self.__twin_solver(left_hand, right_hand, unknown_var)
        return final_ans

    def simple_solver(self, sub_string: str):
        sub_string = self.__basic_solver(sub_string)
        sub_string = self.__complementary_solver(sub_string)
        return sub_string

    ### PRIVATE METHODS ###
    def __basic_solver(self, sub_string: str):
        """
        Recursive function for solving simple equation expressions (substituted)
        i.e. -2+3/2*3 returns 2.5
        Strings with Unknown will be left ignored
        """
        sub_string = self.__string_trimming(sub_string)
        try:
            ans = str(float(sub_string[:-1]))
            return ans
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
                operator_function = self.primary_to_function[operation]
                current_ans = operator_function(value, target)
                final_string = sub_string.replace(
                    f"{value}{operation}{target}", str(current_ans))
                return self.simple_solver(final_string)
            except (KeyError, ValueError):
                return f"({sub_string[:-1]})"
            except Exception as e:
                # Other Kinds of Mathematical Error
                raise Exception(e)

    def __complementary_solver(self, string_equation: str):
        # Getting Rid of Brackets if Given
        string_function = self.__strip_trimming(string_equation)
        low_prior_value = min(list(self.primary_priority.values()))
        for key, item in self.primary_priority.items():
            if item != low_prior_value:
                continue
            string_split = string_function.split(key)
            base = ""
            for index in range(len(string_split)):
                string = string_split[index]
                try:
                    if string_split[index-1][-1] in self.primary_priority.keys():
                        # operation followed by signed number
                        continue
                except IndexError:
                    pass
                current_string = base + string
                current_ans = self.__basic_solver(current_string)
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

    def __index_substring_split(self, sub_string: str, sign):
        """
        Split by sign, returning [index, terms]
        """
        string_split = []
        term = ""
        start_index = 0
        for index in range(len(sub_string+"#")):
            character = (sub_string+"#")[index]
            if character in [sign, "#"] and term:
                string_split.append([start_index, term])
                term, start_index = sign, index
            else:
                term += character
        return string_split

    def __move_low_terms(self, var_side: str, value_side: str):
        low_prior_value = min(list(self.primary_priority.values()))
        for sign, item in self.primary_priority.items():
            if item != low_prior_value:
                continue
            string_split = self.__index_substring_split(var_side, sign)
            for index in range(len(string_split)):
                start_index, string = string_split[index]
                try:
                    if string_split[index-1][1][-1] in self.primary_priority.keys():
                        # operation followed by signed number
                        continue
                except IndexError:
                    pass
                current_ans = self.__basic_solver(string)
                if current_ans[0] == "(" and current_ans[-1] == ")":
                    continue
                else:
                    var_side = var_side[:start_index] + \
                        len(string)*"#" + var_side[start_index+len(string):]
                    value_side += self.inverse_operator[sign] + current_ans
        var_side = self.__strip_trimming(var_side.replace("#", ""))
        value_side = self.simple_solver(value_side)
        return var_side, value_side

    def __equation_solver(self, var_side, value_side, target_variable):
        print(var_side, value_side)
        while var_side != target_variable:
            ### MOVE UNASSOCIATED TERMS ###
            var_side, value_side = self.__move_low_terms(var_side, value_side)
            var_side = self.__strip_trimming(var_side)

            ### MOVE TERMS BASED ON LEVEL ###
            primary_level_dict, secondary_level_dict, variable_level = self.__set_level(
                var_side, target_variable)
            if variable_level != 0:
                var_side, value_side = self.__inverse_operator(
                    primary_level_dict, secondary_level_dict, var_side, value_side)
                continue
            else:
                ### FINAL HANDLING ###
                print(var_side, value_side)
                var_side, value_side = self.__move_low_terms(
                    var_side, value_side)
                print(var_side, value_side)
                break
        return None

    def __inverse_operator(self, primary_level_dict, secondary_level_dict, var_side, value_side):
        if 0 in primary_level_dict.keys():
            resolve_list = primary_level_dict[0]
            for term, end_index, ori_operator, before in resolve_list:
                flip_operator = self.inverse_operator[ori_operator]
                if flip_operator in self.primary_priority.keys() and before:
                    # Primary Operation Before Variable
                    value_side += flip_operator+term
                    value_side = self.simple_solver(value_side)
                    var_side = var_side[:end_index -
                                        len(term)] + "#"*(len(term)+1) + var_side[end_index+1:]
                elif flip_operator in self.primary_priority.keys() and not before:
                    # Primary Operation After Variable
                    value_side += flip_operator+term
                    value_side = self.simple_solver(value_side)
                    var_side = var_side[:end_index -
                                        len(term)-1] + "#"*(len(term)+1) + var_side[end_index:]
                else:
                    # Special Inverse Operator
                    flip_string = flip_operator.replace(
                        "target", value_side).replace("term", term)
                    if before:
                        value_side = self.inverse_log(term, value_side)
                        var_side = var_side[:end_index -
                                            len(term)] + "#"*(len(term)+1) + var_side[end_index+1:]
                    else:
                        operation_key, ori, target = flip_string.split("_")
                        value_side = self.primary_to_function[operation_key](
                            ori, target)
                        var_side = var_side[:end_index -
                                            len(term)-1] + "#"*(len(term)+1) + var_side[end_index:]
        else:
            # Special Bracket List
            term, index = secondary_level_dict[0]
            var_side = self.__strip_trimming(var_side[index:])

            # value side handling
            flip_string = self.inverse_operator[term].replace(
                "target", value_side)
            for special in list(self.special_constants.keys()):
                flip_string = flip_string.replace(
                    special, str(self.special_constants[special]))
            try:
                operation_key, ori, target = flip_string.split("_")
                value_side = self.primary_to_function[operation_key](
                    ori, target)
            except ValueError:
                value_side = self.special_to_function[flip_string](
                    value_side)
        var_side = var_side.replace("#", "")
        return str(var_side), str(value_side)

    def __set_level(self, string_equation: str, target_variable: str):
        string_equation = self.__string_trimming(string_equation)
        split_list = list({**self.primary_priority, **
                          self.secondary_priority}.keys()) + ["#"]  # end indicator
        special_list = self.special_operator
        term, operator, level = "", "", 0
        before = True  # operator order
        consecutive_operator = False  # to prevent negative misplacement

        lvl_term_index_operator = {}
        lvl_special_index = {}
        for index in range(len(string_equation)):
            character = string_equation[index]
            if character not in split_list:
                term += character
            else:
                if character in list(self.secondary_priority.keys()):
                    # Bracket Terms (Different Handling)
                    consecutive_operator = False
                    if term in special_list:
                        # No Two Special Terms on the same Level for one Unknown
                        lvl_special_index[level] = [term, index]
                    elif term:
                        try:
                            lvl_term_index_operator[level].append(
                                [term, index, operator, before])
                        except KeyError:
                            lvl_term_index_operator[level] = [
                                [term, index, operator, before]]
                    level += self.secondary_priority[character]
                elif term:
                    # Primary Operator Terms
                    consecutive_operator = False
                    if term == target_variable:  # variable stage
                        before = False
                        operator = character
                        term = ""
                        variable_level = level
                        continue
                    if before:  # before variable
                        try:
                            lvl_term_index_operator[level].append(
                                [term, index, character, before])
                        except KeyError:
                            lvl_term_index_operator[level] = [
                                [term, index, character, before]]
                    else:  # after variable
                        try:
                            lvl_term_index_operator[level].append(
                                [term, index, operator, before])
                        except KeyError:
                            lvl_term_index_operator[level] = [
                                [term, index, operator, before]]
                        operator = character
                else:
                    # Term Not Defined
                    if consecutive_operator and character != "#":
                        term += character
                        continue
                    else:
                        operator = character
                        consecutive_operator = True
                term = ""
        return dict(sorted(lvl_term_index_operator.items())), dict(sorted(lvl_special_index.items())), variable_level

    def __twin_solver(self, left_hand: str, right_hand: str, target_variable: str):
        """Function to resolve unknown"""
        left_hand = self.__strip_trimming(left_hand)
        right_hand = self.__strip_trimming(right_hand)
        if target_variable in right_hand:
            final_ans = self.__equation_solver(
                right_hand, left_hand, target_variable)
        else:
            final_ans = self.__equation_solver(
                left_hand, right_hand, target_variable)
        return final_ans

    def __string_trimming(self, string_equation: str):
        """
        Process equation expressions
        """
        string_equation = string_equation.lower()
        string_equation = string_equation.replace(" ", "")
        string_equation = string_equation.replace("#", "")
        string_equation = string_equation.replace("**", "^")

        string_equation = re.sub(r"\-\+|\+\-", "-", string_equation)
        string_equation = re.sub(r"\+\+|\-\-", "+", string_equation)

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

    def __strip_trimming(self, string_expression: str):
        """
        Remove covered brackets for better clarity
        Also removed first instance of "+" sign
        """
        if string_expression[0] == "(" and string_expression[-1] == ")":
            if string_expression[1] == "+":
                return string_expression[2:-1]
            return string_expression[1:-1]
        if string_expression[0] == "+":
            return string_expression[1:]
        return string_expression

    def __variable_search(self, string_equation: str, check_list: list):
        string_equation = self.__string_trimming(string_equation)
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

    def __is_valid_equation(self, string_equation: str, index_var_dict: dict):
        """
        Check Validity of Expression in terms of Variables Definition
        """
        string_equation = self.__string_trimming(string_equation)
        copy_dict = copy.deepcopy(index_var_dict)
        variable_count = 0
        for index in list(copy_dict.keys()):
            try:
                float(copy_dict[index])
                del copy_dict[index]
            except ValueError:
                if copy_dict[index] in self.defined_var_dict.keys():
                    variable_count += 1
                    del copy_dict[index]
        if "=" in string_equation:
            # One Argument Short
            if len(copy_dict) != 1:
                return False
        else:
            # Same Argument Count
            if len(copy_dict) != 0:
                return False

        if list(copy_dict.values()):
            # Unknown Instance
            if len(self.defined_var_dict) >= variable_count:
                warnings.warn(
                    "Defined parameters have redundant variables (ignored in calculation).")
            return list(copy_dict.values())[0]
        else:
            # Fixed Instance
            if len(self.defined_var_dict) > variable_count:
                warnings.warn(
                    "Defined parameters have redundant variables (ignored in calculation).")
            return True

    def __set_priority(self, string_equation: str):
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

    def __special_operator_value(self, orig_sub_dict: dict, sub_expression: str):
        """
        Function to execute special operations
        e.g. log10(10) returns 1
        Operation with variables defined in it will be ignored
        """
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
                        special_function = self.special_to_function[special_operator]
                        special_ans = str(special_function(match[0]))
                        orig_sub_dict[special_operator +
                                      match[0]] = special_ans
                        sub_expression = sub_expression.replace(special_operator +
                                                                match[0], special_ans)
        return orig_sub_dict, sub_expression

    def __variable_substitution(self, string_equation: str, sub_index_dict: dict):
        orig_sub_dict = {}
        for _, value in sorted(sub_index_dict.items(), reverse=True):
            pairs = [value[2*ind:2*ind+2] for ind in range(int(len(value)/2))]
            for pair in pairs:
                sub_expression = string_equation[pair[0]:pair[1]+1]
                for key_sub, value_sub in orig_sub_dict.items():
                    sub_expression = sub_expression.replace(
                        key_sub, value_sub)
                orig_sub_dict, sub_expression = self.__special_operator_value(
                    orig_sub_dict, sub_expression)
                final_sub = self.simple_solver(
                    self.__strip_trimming(sub_expression))
                orig_sub_dict[sub_expression] = final_sub
        return orig_sub_dict


'''test = MathSolver(
    "1+2+2/3-exp*2*-(2*a)^3", a=1)
answer = test.linear_solver()
print(answer)'''
test_two = MathSolver(
    "+a*b^2 + sin((2^(3*(1+2+a/b-2*c^(3^2)+2)))*exp*pi^(5/2)+((a/10)))*(-(2^10)) - pi^(5/2) = trial", a=10, b=10, trial=14)
answer_two = test_two.linear_solver()
