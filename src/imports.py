from math import floor, log10


def round_to_sf(value, sf=3):
    rounded_value = round(
        value, sf - int(floor(log10(abs(value)))) - 1)
    return rounded_value
