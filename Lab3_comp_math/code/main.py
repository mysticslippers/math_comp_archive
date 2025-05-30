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


def read_console():
    function_choice = read_function_choice()
    a, b = read_borders()
    initial_approximation = (a, b)
    tolerance = read_tolerance()
    return function_choice, initial_approximation, tolerance


def print_output(method, integral_value, n):
    output_message = f"Метод: {method}, Значение интеграла: {integral_value}, Число разбиения интервала: {n}"
    print(output_message)


def compute_function_value(expression, point):
    value_function = expression.evalf(subs={variable: point})
    return value_function


def compute_integral_value_by_primitive(expression, initial_approximation):
    F_x = sp.integrate(expression(variable), variable)
    F_x_value_at_a = compute_function_value(F_x, initial_approximation[0])
    F_x_value_at_b = compute_function_value(F_x, initial_approximation[1])
    result = F_x_value_at_b - F_x_value_at_a
    print("\nПроверим, посчитав ручками.")
    print(f"Первообразная функции {expression(variable)}: {F_x}")
    print(f"Значение интеграла: {round(result, 5)}")


def compute_integral_value_by_library(expression, initial_approximation):
    result = sp.integrate(expression(variable), (variable, initial_approximation[0], initial_approximation[1]))
    print(f"\nПроверим с помощью библиотеки: {round(result, 5)}")


def left_rectangle_method(function, initial_approximation, tolerance):
    current_result = 0
    n = INITIAL_N

    while n <= INITIAL_N * (2 ** 10):
        previous_result = current_result

        current_result = 0
        x = initial_approximation[0]
        h = (initial_approximation[1] - initial_approximation[0]) / n

        for i in range(n):
            current_result += compute_function_value(function, x)
            x += h
        current_result *= h

        if check_runge_error_estimation(previous_result, current_result, tolerance, 1):
            return current_result, n
        else:
            n *= 2


def middle_rectangle_method(function, initial_approximation, tolerance):
    current_result = 0
    n = INITIAL_N

    while n <= INITIAL_N * (2 ** 10):
        previous_result = current_result

        current_result = 0
        x = initial_approximation[0]
        h = (initial_approximation[1] - initial_approximation[0]) / n

        for i in range(n):
            current_result += compute_function_value(function, x + h / 2)
            x += h
        current_result *= h

        if check_runge_error_estimation(previous_result, current_result, tolerance, 2):
            return current_result, n
        else:
            n *= 2


def right_rectangle_method(function, initial_approximation, tolerance):
    current_result = 0
    n = INITIAL_N

    while n <= INITIAL_N * (2 ** 10):
        previous_result = current_result

        current_result = 0
        x = initial_approximation[0]
        h = (initial_approximation[1] - initial_approximation[0]) / n
        x += h

        for i in range(n + 1):
            current_result += compute_function_value(function, x)
            x += h
        current_result *= h

        if check_runge_error_estimation(previous_result, current_result, tolerance, 1):
            return current_result, n
        else:
            n *= 2


def trapezoidal_method(function, initial_approximation, tolerance):
    current_result = 0
    n = INITIAL_N

    while n <= INITIAL_N * (2 ** 10):
        previous_result = current_result

        x = initial_approximation[0]
        h = (initial_approximation[1] - initial_approximation[0]) / n
        x += h
        current_result = (compute_function_value(function, initial_approximation[0]) + compute_function_value(function, initial_approximation[1])) / 2

        for i in range(n - 1):
            current_result += compute_function_value(function, x)
            x += h
        current_result *= h

        if check_runge_error_estimation(previous_result, current_result, tolerance, 2):
            return current_result, n
        else:
            n *= 2


def simpson_method(function, initial_approximation, tolerance):
    current_result = 0
    n = INITIAL_N

    while n <= INITIAL_N * (2 ** 10):
        previous_result = current_result

        x = initial_approximation[0]
        h = (initial_approximation[1] - initial_approximation[0]) / n
        x += h
        current_result = compute_function_value(function, initial_approximation[0]) + compute_function_value(function, initial_approximation[1])

        for i in range(n - 1):
            if i % 2 == 0:
                current_result += 4 * compute_function_value(function, x)
            else:
                current_result += 2 * compute_function_value(function, x)

            x += h
        current_result *= h / 3

        if check_runge_error_estimation(previous_result, current_result, tolerance, 4):
            return current_result, n
        else:
            n *= 2


def check_runge_error_estimation(previous_result, current_result, tolerance, method):
    diff = abs(current_result - previous_result) / (2 ** method - 1)
    if diff <= tolerance:
        print("\nПравило Рунге сработало.")
        print(f"Значение по правилу Рунге: {round(diff, 5)}")
    return diff <= tolerance


def main():
    print("\t\tЛабораторная работа №3. Численное интегрирование.")
    prompt = "\nВыберите метод для интегрирования: "
    function_choice, initial_approximation, tolerance = read_console()
    function = get_function(function_choice)

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

            method_choice = int(input("\nВведите значение: "))
            if method_choice in method_map:
                result, n = method_map[method_choice](function(variable), initial_approximation, tolerance)
                method_name = method_map[method_choice].__name__.replace('_', ' ').capitalize()
                print_output(method_name, round(result, 5), n)
                compute_integral_value_by_primitive(function, initial_approximation)
                compute_integral_value_by_library(function, initial_approximation)
                break
            else:
                print("Неверный выбор метода! Попробуйте снова.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


if __name__ == '__main__':
    main()
