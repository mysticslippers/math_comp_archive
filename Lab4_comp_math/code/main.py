# Лабораторная работа №4 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

from math import sqrt, log, exp

import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

INPUT_FILE_PATH = "iofiles/input.txt"
OUTPUT_FILE_PATH = "iofiles/output.txt"


def read_dots(prompt="\nВводите координаты через пробел, каждая точка с новой строки.\n"):
    print(prompt)
    print("Чтобы закончить, введите 'END'.")
    dots = []
    while True:
        try:
            current = input("> ").strip()
            if current == "END":
                if len(dots) < 2:
                    raise AttributeError
                return np.array(dots)
            current_dot = tuple(map(float, current.split()))
            if len(current_dot) != 2:
                raise ValueError
            dots.append(current_dot)
        except ValueError:
            print("Введите точку повторно - координаты некорректны!")
        except AttributeError:
            print("Минимальное количество точек - 2!")


def read_file(fila_path=INPUT_FILE_PATH):
    dots = []

    try:
        with open(fila_path, 'rt', encoding='UTF-8') as fin:
            for line in fin:
                current_dot = tuple(map(float, line.strip().split()))
                if len(current_dot) == 2:
                    dots.append(current_dot)
                else:
                    raise ValueError("Каждая строка должна содержать ровно две координаты.")

        if len(dots) < 2:
            raise AttributeError("Недостаточно точек для обработки. Необходимо не менее двух точек.")

    except (ValueError, AttributeError) as exception:
        print(f"Ошибка при обработке файла: {exception}")
        return None

    return dots


def read_input():
    while True:
        try:
            method_choice = input("Выберите способ ввода данных 'файл'/'клавиатура' (+/-): ").strip().lower()
            if method_choice == '+':
                dots = read_file()
                if dots is not None:
                    return dots
                print("Ошибка чтения из файла. Переход к вводу с клавиатуры.")
            elif method_choice == '-':
                return read_dots()
            else:
                print("Некорректный ввод! Попробуйте снова.")
        except Exception as exception:
            print(f"Произошла ошибка: {exception}. Пожалуйста, попробуйте снова.")


def compute_determinant(matrix):
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in matrix[1:]]
        sign = (-1) ** j
        determinant += sign * matrix[0][j] * compute_determinant(minor)

    return determinant


def compute_deviation(dots, function):
    deviations = [(function(dot[0]) - dot[1]) ** 2 for dot in dots]
    return sum(deviations)


def compute_standard_deviation(dots, function):
    n = len(dots)
    if n == 0:
        return 0

    s = compute_deviation(dots, function)
    return sqrt(s / n)


def linear_approximation(dots):
    n = len(dots)

    if n == 0:
        return None

    sx = sum(dot[0] for dot in dots)
    sy = sum(dot[1] for dot in dots)
    sx2 = sum(dot[0] ** 2 for dot in dots)
    sxy = sum(dot[0] * dot[1] for dot in dots)

    determinant = compute_determinant([[sx2, sx], [sx, n]])
    determinant1 = compute_determinant([[sxy, sx], [sy, n]])
    determinant2 = compute_determinant([[sx2, sxy], [sx, sy]])

    if determinant == 0:
        return None

    a = determinant1 / determinant
    b = determinant2 / determinant

    data = {
        'a': a,
        'b': b,
        'f': lambda x: a * x + b,
        'str_f': "f_i = a * x + b",
        's': compute_deviation(dots, lambda x: a * x + b),
        's^2': compute_standard_deviation(dots, lambda x: a * x + b)
    }

    return data


def quadratic_approximation(dots):
    n = len(dots)

    x, y = zip(*dots)

    sx = sum(x)
    sy = sum(y)
    sx2 = sum(xi ** 2 for xi in x)
    sx3 = sum(xi ** 3 for xi in x)
    sx4 = sum(xi ** 4 for xi in x)
    sxy = sum(xi * yi for xi, yi in zip(x, y))
    sx2y = sum((xi ** 2) * yi for xi, yi in zip(x, y))

    determinant = compute_determinant([[n, sx, sx2],
                    [sx, sx2, sx3],
                    [sx2, sx3, sx4]])

    determinant1 = compute_determinant([[sy, sx, sx2],
                     [sxy, sx2, sx3],
                     [sx2y, sx3, sx4]])

    determinant2 = compute_determinant([[n, sy, sx2],
                     [sx, sxy, sx3],
                     [sx2, sx2y, sx4]])

    determinant3 = compute_determinant([[n, sx, sy],
                     [sx, sx2, sxy],
                     [sx2, sx3, sx2y]])

    if determinant == 0:
        return None

    c = determinant1 / determinant
    b = determinant2 / determinant
    a = determinant3 / determinant

    data = {
        'a': a,
        'b': b,
        'c': c,
        'f': lambda x: a * (x ** 2) + b * x + c,
        'str_f': "f_i = a * x^2 + b * x + c",
        's': compute_deviation(dots, lambda x: a * (x ** 2) + b * x + c),
        's^2': compute_standard_deviation(dots, lambda x: a * (x ** 2) + b * x + c)
    }

    return data


def cubic_approximation(dots):
    n = len(dots)

    x, y = zip(*dots)

    sx = sum(x)
    sy = sum(y)
    sx2 = sum(xi ** 2 for xi in x)
    sx3 = sum(xi ** 3 for xi in x)
    sx4 = sum(xi ** 4 for xi in x)
    sx5 = sum(xi ** 5 for xi in x)
    sx6 = sum(xi ** 6 for xi in x)
    sxy = sum(xi * yi for xi, yi in zip(x, y))
    sx2y = sum((xi ** 2) * yi for xi, yi in zip(x, y))
    sx3y = sum((xi ** 3) * yi for xi, yi in zip(x, y))

    determinant = compute_determinant([
        [n, sx, sx2, sx3],
        [sx, sx2, sx3, sx4],
        [sx2, sx3, sx4, sx5],
        [sx3, sx4, sx5, sx6]
    ])

    determinant1 = compute_determinant([
        [sy, sx, sx2, sx3],
        [sxy, sx2, sx3, sx4],
        [sx2y, sx3, sx4, sx5],
        [sx3y, sx4, sx5, sx6]
    ])

    determinant2 = compute_determinant([
        [n, sy, sx2, sx3],
        [sx, sxy, sx3, sx4],
        [sx2, sx2y, sx4, sx5],
        [sx3, sx3y, sx5, sx6]
    ])

    determinant3 = compute_determinant([
        [n, sx, sy, sx3],
        [sx, sx2, sxy, sx4],
        [sx2, sx3, sx2y, sx5],
        [sx3, sx4, sx3y, sx6]
    ])

    if determinant == 0:
        return None

    d = determinant1 / determinant
    c = determinant2 / determinant
    b = determinant3 / determinant
    a = (sy - b * sx - c * sx2 - d * sx3) / n

    data = {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'f': lambda x: a * (x ** 3) + b * (x ** 2) + c * x + d,
        'str_f': "f_i = a * x^3 + b * x^2 + c * x + d",
        's': compute_deviation(dots, lambda x: a * (x ** 3) + b * (x ** 2) + c * x + d),
        's^2': compute_standard_deviation(dots, lambda x: a * (x ** 3) + b * (x ** 2) + c * x + d)
    }

    return data


def exponential_approximation(dots):
    dots_array = np.array(dots)

    if not dots_array.size or np.any(dots_array[:, 1] <= 0):
        return None

    x = [dot[0] for dot in dots]
    lin_y = [log(dot[1]) for dot in dots]

    lin_result = linear_approximation(list(zip(x, lin_y)))

    a = exp(lin_result['b'])
    b = lin_result['a']

    data = {
        'a': a,
        'b': b,
        'f': lambda x: a * exp(b * x),
        'str_f': "f_i = a * e^(b * x)",
        's': compute_deviation(dots, lambda x: a * exp(b * x)),
        's^2': compute_standard_deviation(dots, lambda x: a * exp(b * x))
    }

    return data


def logarithmic_approximation(dots):
    dots_array = np.array(dots)

    if not dots_array.size or np.any(dots_array[:, 0] <= 0):
        return None

    x = [dot[0] for dot in dots]
    y = [dot[1] for dot in dots]

    lin_x = [log(val) for val in x]
    lin_result = linear_approximation(list(zip(lin_x, y)))

    a = lin_result['a']
    b = lin_result['b']

    data = {
        'a': a,
        'b': b,
        'f': lambda x: a * log(x) + b,
        'str_f': "f_i = a * ln(x) + b",
        's': compute_deviation(dots, lambda x: a * log(x) + b),
        's^2': compute_standard_deviation(dots, lambda x: a * log(x) + b)
    }

    return data


def power_approximation(dots):
    dots_array = np.array(dots)
    if np.any(dots_array[:, 0] <= 0) or np.any(dots_array[:, 1] <= 0):
        return None

    lin_x = [log(dot[0]) for dot in dots]
    lin_y = [log(dot[1]) for dot in dots]

    lin_result = linear_approximation(list(zip(lin_x, lin_y)))

    a = exp(lin_result['b'])
    b = lin_result['a']

    data = {
        'a': a,
        'b': b,
        'f': lambda x: a * (x ** b),
        'str_f': "f_i = a * x^b",
        's': compute_deviation(dots, lambda x: a * (x ** b)),
        's^2': compute_standard_deviation(dots, lambda x: a * (x ** b))
    }

    return data


def print_output(table1, table2, output_to_file, filename=OUTPUT_FILE_PATH):
    output_message = table1.get_string() + "\n\n" + table2.get_string()
    if output_to_file:
        with open(filename, 'w') as file:
            file.write(output_message)
    else:
        print(output_message)


def plot(x, y, plot_x, plot_ys, labels):
    plt.figure()
    plt.title("График")

    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.plot(1, 0, marker='>', markersize=5, color='k', transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker='^', markersize=5, color='k', transform=ax.get_xaxis_transform(), clip_on=False)

    plt.scatter(x, y, marker='o', color='b', label='Данные')

    for plot_y, label in zip(plot_ys, labels):
        plt.plot(plot_x, plot_y, label=label)

    plt.legend()
    plt.grid(True)
    plt.show(block=False)


def main():
    print("\t\t\t\tЛабораторная работа №4")
    dots = read_input()

    answers = []
    tmp_answers = [linear_approximation(dots),
                   quadratic_approximation(dots),
                   exponential_approximation(dots),
                   logarithmic_approximation(dots),
                   power_approximation(dots)]

    for answer in tmp_answers:
        if answer is not None:
            answers.append(answer)

    table1 = PrettyTable()
    table1.field_names = ["Вид функции", "Ср. отклонение"]
    for answer in answers:
        table1.add_row([answer['str_f'], f"{answer['s^2']:.4f}"])

    x = np.array([dot[0] for dot in dots])
    y = np.array([dot[1] for dot in dots])
    plot_x = np.linspace(np.min(x), np.max(x), 100)
    plot_y = []
    labels = []

    for answer in answers:
        plot_y.append([answer['f'](x) for x in plot_x])
        labels.append(answer['str_f'])

    plot(x, y, plot_x, plot_y, labels)

    best_answer = min(answers, key=lambda x: x['s^2'])

    table2 = PrettyTable()
    table2.field_names = ["Параметр", "Значение"]
    table2.add_row(["Наилучшая аппроксимирующая функция", best_answer['str_f']])
    table2.add_row(["a", round(best_answer['a'], 4)])
    table2.add_row(["b", round(best_answer['b'], 4)])
    table2.add_row(["c", round(best_answer['c'], 4) if 'c' in best_answer else '-'])

    output_to_file = input("Вывести результаты в файл? (y/n): ").strip().lower() == 'y'
    print_output(table1, table2, output_to_file)


if __name__ == "__main__":
    main()
