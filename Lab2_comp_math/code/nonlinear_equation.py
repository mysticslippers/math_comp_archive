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


def list_functions():
    functions = [
        "1. cos(x) - x",
        "2. x^3 - x - 2",
        "3. exp(x) - 3*x^2",
        "4. x^2 - 2",
        "5. log(x + 2) - x"
    ]
    print("\n".join(functions))


def read_function_choice(prompt="Выберите номер функции (1-5): "):
    list_functions()

    while True:
        try:
            function_choice = int(input(prompt))
            if 1 <= function_choice <= 5:
                return function_choice
            else:
                print("Некорректный выбор функции! Попробуйте снова.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_borders(function_choice):
    try:
        a = float(input("Введите левую границу интервала (a): "))
        b = float(input("Введите правую границу интервала (b): "))

        func = get_function(function_choice)

        if not verify_root(func, a, b):
            print("Некорректный ввод! Попробуйте снова.")
            return read_borders(function_choice)

        return a, b
    except ValueError:
        print("Ошибка ввода! Пожалуйста, введите числовые значения.")
        return read_borders(function_choice)


def read_tolerance(prompt="Введите допустимую погрешность (0 < tolerance <= 1): "):
    while True:
        try:
            tolerance = float(input(prompt))
            if 0 < tolerance <= 1:
                return tolerance
            else:
                print("Некорректный ввод! Пожалуйста, введите значение в диапазоне от 0 до 1.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_initial_approximation(prompt="Введите допустимое начальное приближение: "):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")
