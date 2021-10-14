import queue
from math import floor, log10


def round_to_sf(value, sf=3):
    rounded_value = round(
        value, sf - int(floor(log10(abs(value)))) - 1)
    return rounded_value


def find_variables(string_equation, primary_priority, secondary_priority):
    string_equation += "#"
    index_variable_dict, variable_string = {}, ""
    for character_index in range(len(string_equation)):
        character = string_equation[character_index]
        if character not in {**primary_priority, **secondary_priority} .keys():
            variable_string += character
        else:
            # operator in between
            if variable_string not in "":
                start_index = character_index - len(variable_string)
                index_variable_dict[start_index] = variable_string
                variable_string = ""
    return index_variable_dict


def is_valid_equation(string_equation, index_variable_dict, variable_dict):
    valid_counter = 0
    for index in list(index_variable_dict.keys()):
        try:
            float(index_variable_dict[index])  # numbers handling
        except ValueError:
            valid_counter += 1  # dict must contain variable
    if "=" in string_equation:
        if valid_counter != len(variable_dict)+1:   # always one argument short
            return False
    else:
        if valid_counter != len(variable_dict):     # equal argument number
            return False
    return True


def simple_solver(string_equation, **variable_dict):
    """
    Function for resolving one unknown variable from equation
    Example:
    string = "(x + 2) / y = ( z + 1 )^-1"
    variable = {x = 1, y = 2}
    Automatically detect unkown z variable and solve it
    """
    # basic mathemtical operation
    primary_priority = {"+": 0, "-": 0, "*": 1, "/": 1, "^": 1, "=": None}

    # brackets operation
    secondary_priority = {
        "(": 2, ")": 2,
        "[": 2, "]": 2,
        "{": 2, "}": 2,
        "#": None,
    }
    string_equation = string_equation.replace(" ", "")
    # variable search
    index_variable_dict = find_variables(
        string_equation, primary_priority, secondary_priority)
    # check valid equation
    if not is_valid_equation(string_equation, index_variable_dict, variable_dict):
        raise Exception("Not enough arguments to resolve equation")
    # find index and replace string with unkown
    for index in index_variable_dict:
        variable = index_variable_dict[index]
        string_equation = string_equation.replace(
            variable, "#"*len(variable), 1)
    print(string_equation)


simple_solver("{(  2 +  adsf )}/2  } = 2")
