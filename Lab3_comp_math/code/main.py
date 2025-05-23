# Лабораторная работа №3 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

import sympy as sp

INITIAL_N = 4
variable = sp.symbols('x')

def f1(x):
    return x**2 - 1


def f2(x):
    return sp.sin(x)


def f3(x):
    return x**3 - 3 * x**2 + 6 * x - 19


def f4(x):
    return sp.cos(x)


def f5(x):
    return sp.ln(x + 1)
