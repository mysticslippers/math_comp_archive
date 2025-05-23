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


def read_function_choice(prompt="\nВыберите номер функции (1-5): "):
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


def read_borders():
    while True:
        try:
            a = float(input("\nВведите нижнюю границу интегрирования (a): "))
            b = float(input("Введите верхнюю границу интегрирования (b): "))
            if a > b:
                a, b = b, a

            return a, b
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовые значения.")


def read_tolerance(prompt="\nВведите допустимую погрешность (0 < tolerance <= 1): "):
    while True:
        try:
            tolerance = float(input(prompt))
            if 0 < tolerance <= 1:
                return tolerance
            else:
                print("Некорректный ввод! Пожалуйста, введите значение в диапазоне от 0 до 1.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_method(prompt="\nВыберите метод для интегрирования: "):
    while True:
        try:
            method_map = {
                1: left_rectangle_method,
                2: middle_rectangle_method,
                3: right_rectangle_method,
                4: trapezoidal_method,
                5: simpson_method
            }
            print(prompt)
            for key, method in method_map.items():
                print(f"{key}. Метод {method.__name__.replace('_', ' ').capitalize()}")

            method_choice = int(input())
            if method_choice in method_map:
                return method_map.get(method_choice, None)
            else:
                print("Неверный выбор метода! Попробуйте снова.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_console():
    function_choice = read_function_choice()
    a, b = read_borders()
    initial_approximation = (a, b)
    tolerance = read_tolerance()
    method_choice = read_method()
    return function_choice, initial_approximation, tolerance, method_choice


def print_output(method, integral_value, n):
    output_message = f"Метод: {method}, Значение интеграла: {integral_value}, Число разбиения интервала: {n}"
    print(output_message)


def compute_function_value(expression, point):
    function = expression(variable)
    value_function = function.evalf(subs={variable: point})
    return value_function


def left_rectangle_method(function, initial_approximation, tolerance):
    current_result = 0
    n = INITIAL_N

    while n <= n * (2 ** 10):
        previous_result = current_result

        current_result = 0
        x = initial_approximation[0]
        h = (initial_approximation[1] - initial_approximation[0]) / n

        for i in range(n):
            current_result += compute_function_value(function, x)
            x += h
        current_result *= h

        if check_runge_error_estimation(previous_result, current_result, tolerance, 2):
            return current_result, n
        else:
            n *= 2
