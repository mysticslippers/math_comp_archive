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

    fa, fb = compute_function_value(expression(variable), a), compute_function_value(expression(variable), b)

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


def find_lamda_coefficient(expression, borders):
    derivative = find_derivative(expression)

    value_derivative_at_left = round(abs(compute_function_value(derivative, borders[0])), 2)
    print(f"Значение производной функции f'(x) на левой границе: {value_derivative_at_left}")

    value_derivative_at_right = round(abs(compute_function_value(derivative, borders[1])), 2)
    print(f"Значение производной функции f'(x) на правой границе: {value_derivative_at_right}")

    if value_derivative_at_left == 0 or value_derivative_at_right == 0:
        raise ValueError("Производная равна нулю, деление на ноль не допускается!")


    maximum = value_derivative_at_left if (value_derivative_at_left > value_derivative_at_right) else value_derivative_at_right

    return -1 / maximum


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
    while True:
        root = (a + b) / 2.0
        f_root = function(root)

        if abs(f_root) <= tolerance:
            return root, f_root, iterations
        elif function(a) * f_root > 0:
            a = root
        else:
            b = root

        iterations += 1


def newton_method(function, a, b, tolerance, max_iterations=10000):
    iterations = 0
    derivative = find_derivative(function)
    print(f"\nПроизводная функции: {derivative}")
    second_derivative = find_second_derivative(function)
    print(f"Вторая производная функции: {second_derivative}\n")

    current_guess = a if compute_function_value(function(variable), a) * compute_function_value(second_derivative, a) > 0 else b
    print(f"x_0 = {current_guess}")

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

        if abs(next_guess - current_guess) <= tolerance and abs(
                f_next_guess_value / f_next_guess_derivative_value) <= tolerance and abs(
                f_next_guess_value) <= tolerance:
            return next_guess, f_next_guess_value, iterations

        current_guess = next_guess
        iterations += 1

    raise ValueError("Метод Ньютона не сошелся за максимальное количество итераций!")


def iteration_method(function, initial_approximation, tolerance, max_iterations=10000):
    iterations = 0
    a, b = initial_approximation[0], initial_approximation[1]
    derivative = find_derivative(function)
    print(f"\nПроизводная функции: {derivative}")
    second_derivative = find_second_derivative(function)
    print(f"Вторая производная функции: {second_derivative}\n")

    lamda = round(find_lamda_coefficient(function, initial_approximation), 2)
    print(f"Коэффициент лямбда: {lamda}\n")

    def phi_function(x):
        function_value = compute_function_value(function(variable), x)
        return x + lamda * function_value


    def check_convergence():
        phi_derivative_value_left = abs(1 + lamda * compute_function_value(derivative, a))
        print(f"Значение производной функции phi'(x) на левой границе: {phi_derivative_value_left}")

        phi_derivative_value_right = abs(1 + lamda * compute_function_value(derivative, b))
        print(f"Значение производной функции phi'(x) на правой границе: {phi_derivative_value_right}")

        q = phi_derivative_value_left if (phi_derivative_value_left > phi_derivative_value_right) else phi_derivative_value_right
        return q >= 1


    if check_convergence():
        return None, None, None

    current_value = a if compute_function_value(function(variable), a) * compute_function_value(second_derivative, a) > 0 else b
    print(f"x_0 = {current_value}")

    while iterations < max_iterations:
        next_value = phi_function(current_value)

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
