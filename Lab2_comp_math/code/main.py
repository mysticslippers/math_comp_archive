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


def get_function(choice):
    functions = {
        1: f1,
        2: f2,
        3: f3,
        4: f4,
        5: f5
    }
    return functions.get(choice, None)


def verify_root(expression, a, b):
    fa, fb = expression(a), expression(b)

    if fa * fb > 0:
        print("На заданном интервале нет корня или несколько корней!")
        return False

    print(f"Есть корень уравнения на интервале [{a}, {b}].")
    return True


def find_derivative(expression):
    return sp.diff(expression(variable), variable)


def compute_function_value(expression, point):
    function = expression(variable)
    value_function = function.evalf(subs={variable: point})
    return value_function


def find_g_function_at_point(expression, point):
    value_function = compute_function_value(expression, point)
    derivative = find_derivative(expression)
    value_derivative = value_function(derivative)

    if value_derivative == 0:
        raise ValueError("Производная равна нулю, деление на ноль не допускается!")

    value = point + (-1 / value_derivative) * value_function
    return value


def plot_function(f, a, b, num_points=1000, title='График функции', xlabel='x', ylabel='f(x)', line_style='-',
                  line_color='b'):

    if not callable(f):
        raise ValueError("Параметр 'f' должен быть вызываемым объектом (функция).")
    if a >= b:
        raise ValueError("Параметр 'a' должен быть меньше параметра 'b'.")

    x = np.linspace(a, b, num_points)

    try:
        y = f(x)
    except Exception as e:
        raise RuntimeError(f"Ошибка при вычислении значений функции: {e}")

    plt.plot(x, y, label='Функция', linestyle=line_style, color=line_color)
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()


def bisection_method(function, a, b, tolerance):
    iterations, root = 0, 0
    while abs(b - a) > tolerance or function((a + b) / 2.0) > 0:
        root = (a + b) / 2.0
        f_root = function(root)

        if f_root == 0:
            return root, f_root, iterations
        elif function(a) * f_root > 0:
            a = root
        else:
            b = root

        iterations += 1

    return root, function(root), iterations
