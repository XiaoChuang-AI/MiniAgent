from string import Formatter


def get_variables_from_str(input_string):
    variables = {v for _, v, _, _ in Formatter().parse(input_string) if v is not None}
    return variables

