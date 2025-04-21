# Лабораторная работа №2 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

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


def read_function_choice():
    list_functions()

    while True:
        try:
            function_choice = int(input("Выберите номер функции (1-5): "))
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


def read_tolerance():
    while True:
        try:
            tolerance = float(input("Введите допустимую погрешность (0 < tolerance <= 1): "))
            if 0 < tolerance <= 1:
                return tolerance
            else:
                print("Некорректный ввод! Пожалуйста, введите значение в диапазоне от 0 до 1.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_console():
    function_choice = read_function_choice()
    a, b = read_borders(function_choice)
    tolerance = read_tolerance()
    return function_choice, a, b, tolerance


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            function_choice = int(lines[0].strip())
            a = float(lines[1].strip())
            b = float(lines[2].strip())
            tolerance = float(lines[3].strip())

            func = get_function(function_choice)
            if not verify_root(func, a, b):
                print("Некорректный ввод! Режим ввода переключён на консоль.")
                return None

            return function_choice, a, b, tolerance
    except (ValueError, IndexError, FileNotFoundError) as e:
        print(f"Ошибка при чтении файла: {e}. Режим ввода переключён на консоль.")
        return None


def read_input():
    while True:
        method_choice = input("Выберите способ ввода данных 'файл'/'клавиатура' (+/-): ").strip().lower()

        if method_choice == '+':
            function_choice, a, b, tolerance = read_file(INPUT_FILE_PATH)
            if function_choice is not None:
                return function_choice, a, b, tolerance
            print("Ошибка чтения из файла. Переход к вводу с клавиатуры.")

        elif method_choice == '-':
            return read_console()

        else:
            print("Некорректный ввод! Попробуйте снова.")
