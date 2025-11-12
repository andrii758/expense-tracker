import argparse


def positive_int(value):
    int_value = int(value)
    if int_value < 1:
        raise argparse.ArgumentTypeError(f"Value must be >= 1, received {value}")
    return int_value
