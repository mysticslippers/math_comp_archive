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


def read_console():
    function_choice = read_function_choice()
    a, b = read_borders(function_choice)
    tolerance = read_tolerance()
    return function_choice, a, b, tolerance


def read_file(file_path=INPUT_FILE_PATH):
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
            function_choice, a, b, tolerance = read_file()
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


def is_logarithmic(expression):
    function = expression(variable)
    return function.has(sp.log)


def verify_root(expression, a, b):
    if is_logarithmic(expression):
        if a <= -2 or b <= -2:
            print(f"Интервал [{a}, {b}] содержит значения, для которых логарифм не определен.")
            return False

    fa, fb = expression(a), expression(b)

    if fa * fb > 0:
        print("На заданном интервале нет корня или несколько корней!")
        return False

    print(f"Есть корень уравнения на интервале [{a}, {b}].")
    return True


def find_derivative(expression):
    return sp.diff(expression(variable), variable)


def find_second_derivative(expression):
    first_derivative = sp.diff(expression(variable), variable)
    return sp.diff(first_derivative, variable)


def compute_function_value(expression, point):
    value_function = expression.evalf(subs={variable: point})
    return value_function


def find_g_function_at_point(expression, point):
    value_function = compute_function_value(expression(variable), point)
    derivative = find_derivative(expression)
    value_derivative = compute_function_value(derivative, point)

    if value_derivative == 0:
        raise ValueError("Производная равна нулю, деление на ноль не допускается!")

    value = point + (-1 / value_derivative) * value_function
    return value


def plot(function, a, b, num_points=1000, title='График функции', xlabel='x', ylabel='f(x)', line_style='-',
                  line_color='b'):
    if not callable(function):
        raise ValueError("Параметр 'f' должен быть вызываемым объектом (функция).")
    if a >= b:
        raise ValueError("Параметр 'a' должен быть меньше параметра 'b'.")

    points = np.linspace(a, b, num_points)

    try:
        y = np.array([compute_function_value(function(variable), point) for point in points])
    except Exception as e:
        raise RuntimeError(f"Ошибка при вычислении значений функции: {e}")

    plt.plot(points, y, label='Функция', linestyle=line_style, color=line_color)
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()


def print_output(method, root, func_value, iterations, output_to_file, filename=OUTPUT_FILE_PATH):
    output_message = f"Method: {method}, Root: {root}, The value of the function at the root: {func_value}, Number of iterations: {iterations}"
    if output_to_file:
        with open(filename, 'w') as file:
            file.write(output_message)
    else:
        print(output_message)


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


def newton_method(function, a, b, tolerance, max_iterations=10000):
    iterations = 0
    derivative = find_derivative(function)
    second_derivative = find_second_derivative(function)

    current_guess = a if compute_function_value(function(variable), a) * compute_function_value(second_derivative, a) > 0 else b

    while iterations < max_iterations:
        f_value = compute_function_value(function(variable), current_guess)
        f_derivative_value = compute_function_value(derivative, current_guess)

        if f_derivative_value == 0:
            raise ValueError("Производная равна нулю! Метод не может продолжаться!")

        next_guess = current_guess - (f_value / f_derivative_value)

        f_next_guess_value = compute_function_value(function(variable), next_guess)
        f_next_guess_derivative_value = compute_function_value(derivative, next_guess)

        if f_next_guess_derivative_value == 0:
            raise ValueError("Производная равна нулю! Метод не может продолжаться!")

        if abs(next_guess - current_guess) <= tolerance or abs(
                f_next_guess_value / f_next_guess_derivative_value) <= tolerance or abs(
                f_next_guess_value) <= tolerance:
            return next_guess, f_next_guess_value, iterations

        current_guess = next_guess
        iterations += 1

    raise ValueError("Метод Ньютона не сошелся за максимальное количество итераций!")


def iteration_method(function, initial_approximation, tolerance, max_iterations=10000):
    iterations = 0
    current_value = initial_approximation
    derivative = find_derivative(function)

    while iterations < max_iterations:
        next_value = find_g_function_at_point(function, current_value)
        f_derivative_value = compute_function_value(derivative, next_value)

        if abs(f_derivative_value) >= 1:
            return None, None, None

        if abs(next_value - current_value) <= tolerance:
            f_next_value = compute_function_value(function(variable), next_value)
            return next_value, f_next_value, iterations

        current_value = next_value
        iterations += 1

    return None, None, None


def solve_nonlinear_equation():
    print("\t\tЧисленное решение нелинейных уравнений")
    function_choice, a, b, tolerance = read_input()
    function = get_function(function_choice)

    method_map = {
        1: bisection_method,
        2: newton_method,
        3: iteration_method
    }

    print("Выберите метод:")
    for key, method in method_map.items():
        print(f"{key}. Метод {method.__name__.replace('_', ' ').capitalize()}")

    while True:
        try:
            method_choice = int(input("Ваш выбор: "))
            if method_choice not in method_map:
                print("Неверный выбор метода! Попробуйте снова.")
                continue

            if method_choice == 3:
                initial_approximation = read_initial_approximation()
                root, f_value, iterations = iteration_method(function, initial_approximation, tolerance)
                if root is None:
                    print("Не выполняется условие сходимости!")
                    continue
            else:
                root, f_value, iterations = method_map[method_choice](function, a, b, tolerance)

            output_to_file = input("Вывести результаты в файл? (y/n): ").strip().lower() == 'y'
            print_output(method_choice, root, f_value, iterations, output_to_file)

            plot(function, a, b)
            break

        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")
