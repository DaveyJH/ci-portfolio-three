"""Creates matrix style lines of 1s and 0s."""

from random import randrange
from time import sleep

MATRIX_CHARS = (1, 0)


def matrix_line():
    """Print a random line of 60 1s and 0s followed by a 0.5s delay."""

    line = ""
    for n in range(80):
        line = line + (str(MATRIX_CHARS[
            randrange(len(MATRIX_CHARS))]))
    print(line)
    sleep(.5)


def matrix_block(num: int = 5):
    """Print block of matrix lines.

    ---
    Args:
        num (int): (default = 5) Integer value determining how many lines to
        print.
    """

    for n in range(num):
        matrix_line()
