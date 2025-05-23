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


def list_functions():
    functions = [
        "1. x^2 - 1",
        "2. sin(x)",
        "3. x^3 - 3x^2 + 6x - 19",
        "4. cos(x)",
        "5. ln(x + 1)"
    ]
    print("\n".join(functions))


def get_function(choice):
    functions = {
        1: f1,
        2: f2,
        3: f3,
        4: f4,
        5: f5
    }
    return functions.get(choice, None)


def get_method(choice):
    method_map = {
        1: left_rectangle_method,
        2: middle_rectangle_method,
        3: right_rectangle_method,
        4: trapezoidal_method,
        5: simpson_method
    }
    return method_map.get(choice, None)
