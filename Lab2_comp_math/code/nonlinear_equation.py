import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

variable = sp.symbols('x')
INPUT_FILE_PATH = "iofiles/input.txt"
OUTPUT_FILE_PATH = "iofiles/output.txt"

def f1(x):
    return sp.cos(x) - x


def f2(x):
    return x ** 3 - x - 2


def f3(x):
    return sp.exp(x) - 3 * x ** 2


def f4(x):
    return x ** 2 - 2


def f5(x):
    return sp.log(x + 2) - x
