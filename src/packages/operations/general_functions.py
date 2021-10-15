import math


def round_to_sf(value, sf=3):
    rounded_value = round(
        value, sf - int(math.floor(math.log10(abs(value)))) - 1)
    return rounded_value
