import math
import os
from typing import Callable, List, Optional, Tuple

import matplotlib.pyplot as plt


EPS = 1e-12


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: нужно ввести целое число.")


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("Ошибка: нужно ввести число.")


def input_float_list(prompt: str) -> list[float] | None:
    while True:
        try:
            raw = input(prompt).strip().replace(",", ".")
            values = [float(x) for x in raw.split()]
            if not values:
                print("Ошибка: список не должен быть пустым.")
                continue
            return values
        except ValueError:
            print("Ошибка: введите числа через пробел.")


def pause() -> None:
    input("\nНажмите Enter, чтобы продолжить...")


def check_unique_x(xs: List[float]) -> None:
    if len(set(xs)) != len(xs):
        raise ValueError("Значения x должны быть уникальными.")


def sort_points(xs: List[float], ys: List[float]) -> Tuple[List[float], List[float]]:
    pairs = sorted(zip(xs, ys), key=lambda p: p[0])
    return [p[0] for p in pairs], [p[1] for p in pairs]


def is_equally_spaced(xs: List[float], eps: float = 1e-9) -> bool:
    if len(xs) < 2:
        return True
    h = xs[1] - xs[0]
    for i in range(1, len(xs) - 1):
        if abs((xs[i + 1] - xs[i]) - h) > eps:
            return False
    return True


def factorial(n: int) -> int:
    return math.factorial(n)


def get_variant_12_data() -> Tuple[List[float], List[float]]:
    xs = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
    ys = [1.5320, 2.5356, 3.5406, 4.5462, 5.5504, 6.5559, 7.5594]
    return xs, ys



def input_data_from_keyboard() -> Tuple[List[float], List[float], Optional[Callable[[float], float]]]:
    print("\nВвод таблицы с клавиатуры")
    n = input_int("Введите количество точек: ")

    if n < 2:
        raise ValueError("Количество точек должно быть не меньше 2.")

    xs = input_float_list("Введите x через пробел: ")
    ys = input_float_list("Введите y через пробел: ")

    if len(xs) != n or len(ys) != n:
        raise ValueError("Количество введённых x и y должно совпадать с n.")

    check_unique_x(xs)
    xs, ys = sort_points(xs, ys)
    return xs, ys, None


def input_data_from_file() -> Tuple[List[float], List[float], Optional[Callable[[float], float]]]:
    print("\nВвод таблицы из файла")
    print("Формат файла:")
    print("1 строка: x через пробел")
    print("2 строка: y через пробел")

    filename = input("Введите путь к файлу: ").strip()

    if not os.path.exists(filename):
        raise FileNotFoundError("Файл не найден.")

    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    if len(lines) < 2:
        raise ValueError("В файле должно быть минимум 2 непустые строки.")

    xs = [float(x) for x in lines[0].replace(",", ".").split()]
    ys = [float(y) for y in lines[1].replace(",", ".").split()]

    if len(xs) != len(ys):
        raise ValueError("Количество x и y в файле должно совпадать.")

    if len(xs) < 2:
        raise ValueError("Нужно минимум 2 точки.")

    check_unique_x(xs)
    xs, ys = sort_points(xs, ys)
    return xs, ys, None


def choose_function_data() -> Tuple[List[float], List[float], Optional[Callable[[float], float]]]:
    print("\nВыберите функцию:")
    print("1. sin(x)")
    print("2. cos(x)")
    print("3. e^x")
    print("4. x^2")

    choice = input_int("Введите номер функции (1-4): ")

    if choice == 1:
        function = math.sin
        function_name = "sin(x)"
    elif choice == 2:
        function = math.cos
        function_name = "cos(x)"
    elif choice == 3:
        function = math.exp
        function_name = "e^x"
    elif choice == 4:
        function = lambda x: x ** 2
        function_name = "x^2"
    else:
        raise ValueError("Некорректный выбор функции.")

    a = input_float("Введите левую границу интервала a: ")
    b = input_float("Введите правую границу интервала b: ")
    n = input_int("Введите количество точек: ")

    if n < 2:
        raise ValueError("Количество точек должно быть не меньше 2.")
    if a >= b:
        raise ValueError("Должно выполняться a < b.")

    h = (b - a) / (n - 1)
    xs = [a + i * h for i in range(n)]
    ys = [function(x) for x in xs]

    print(f"Таблица сформирована для функции {function_name}.")
    return xs, ys, function


def finite_differences_table(ys: List[float]) -> List[List[float]]:
    table = [ys[:]]
    current = ys[:]

    while len(current) > 1:
        next_row = [current[i + 1] - current[i] for i in range(len(current) - 1)]
        table.append(next_row)
        current = next_row

    return table


def divided_differences_table(xs: List[float], ys: List[float]) -> List[List[float]]:
    n = len(xs)
    table = [ys[:]]

    for order in range(1, n):
        prev = table[order - 1]
        curr = []
        for i in range(n - order):
            denominator = xs[i + order] - xs[i]
            if abs(denominator) < EPS:
                raise ZeroDivisionError("Совпадающие x при вычислении разделённых разностей.")
            curr.append((prev[i + 1] - prev[i]) / denominator)
        table.append(curr)

    return table


def print_source_table(xs: List[float], ys: List[float]) -> None:
    print("\nИсходная таблица:")
    print(f"{'i':>5}{'x':>15}{'y':>15}")
    for i, (x, y) in enumerate(zip(xs, ys)):
        print(f"{i:>5}{x:>15.6f}{y:>15.6f}")


def print_finite_differences(xs: List[float], ys: List[float]) -> None:
    diffs = finite_differences_table(ys)
    n = len(xs)

    print("\nТаблица конечных разностей:")
    header = ["i", "x", "y"] + [f"Δ^{k}y" for k in range(1, n)]
    print("".join(f"{h:>14}" for h in header))

    for i in range(n):
        row = [str(i), f"{xs[i]:.6f}", f"{ys[i]:.6f}"]
        for k in range(1, n):
            if i < len(diffs[k]):
                row.append(f"{diffs[k][i]:.6f}")
            else:
                row.append("")
        print("".join(f"{cell:>14}" for cell in row))


def lagrange_interpolation(xs: List[float], ys: List[float], x: float) -> float:
    n = len(xs)
    result = 0.0

    for i in range(n):
        term = ys[i]
        for j in range(n):
            if i != j:
                denominator = xs[i] - xs[j]
                if abs(denominator) < EPS:
                    raise ZeroDivisionError("Совпадающие узлы в формуле Лагранжа.")
                term *= (x - xs[j]) / denominator
        result += term

    return result



def newton_divided_interpolation(xs: List[float], ys: List[float], x: float) -> float:
    dd = divided_differences_table(xs, ys)
    n = len(xs)

    result = dd[0][0]
    product = 1.0

    for order in range(1, n):
        product *= (x - xs[order - 1])
        result += dd[order][0] * product

    return result



def gauss_forward_interpolation(xs: List[float], ys: List[float], x: float) -> float:
    if not is_equally_spaced(xs):
        raise ValueError("Формула Гаусса применима только для равноотстоящих узлов.")

    delta = finite_differences_table(ys)
    n = len(xs)
    h = xs[1] - xs[0]
    m = n // 2
    x0 = xs[m]
    t = (x - x0) / h

    result = ys[m]

    if m < len(delta[1]):
        result += t * delta[1][m]

    for k in range(2, n):
        if k % 2 == 0:
            start_index = m - k // 2
            factors = []
            for j in range(k):
                if j == 0:
                    factors.append(t)
                else:
                    shift = j // 2
                    if j % 2 == 1:
                        factors.append(t - shift)
                    else:
                        factors.append(t + shift)
        else:
            start_index = m - (k - 1) // 2
            factors = []
            for j in range(k):
                if j == 0:
                    factors.append(t)
                else:
                    shift = (j + 1) // 2
                    if j % 2 == 1:
                        factors.append(t + shift)
                    else:
                        factors.append(t - shift)

        if 0 <= start_index < len(delta[k]):
            product = 1.0
            for factor in factors:
                product *= factor
            result += product * delta[k][start_index] / factorial(k)

    return result


def gauss_backward_interpolation(xs: List[float], ys: List[float], x: float) -> float:
    if not is_equally_spaced(xs):
        raise ValueError("Формула Гаусса применима только для равноотстоящих узлов.")

    delta = finite_differences_table(ys)
    n = len(xs)
    h = xs[1] - xs[0]
    m = n // 2
    x0 = xs[m]
    t = (x - x0) / h

    result = ys[m]

    if 0 <= m - 1 < len(delta[1]):
        result += t * delta[1][m - 1]

    for k in range(2, n):
        if k % 2 == 0:
            start_index = m - k // 2
            factors = []
            for j in range(k):
                if j == 0:
                    factors.append(t)
                else:
                    shift = j // 2
                    if j % 2 == 1:
                        factors.append(t + shift)
                    else:
                        factors.append(t - shift)
        else:
            start_index = m - (k + 1) // 2
            factors = []
            for j in range(k):
                if j == 0:
                    factors.append(t)
                else:
                    shift = (j + 1) // 2
                    if j % 2 == 1:
                        factors.append(t - shift)
                    else:
                        factors.append(t + shift)

        if 0 <= start_index < len(delta[k]):
            product = 1.0
            for factor in factors:
                product *= factor
            result += product * delta[k][start_index] / factorial(k)

    return result


def gauss_interpolation_auto(xs: List[float], ys: List[float], x: float) -> Tuple[float, str]:
    m = len(xs) // 2
    if x >= xs[m]:
        return gauss_forward_interpolation(xs, ys, x), "1-я формула Гаусса"
    return gauss_backward_interpolation(xs, ys, x), "2-я формула Гаусса"



def plot_interpolation(
    xs: List[float],
    ys: List[float],
    x_query: Optional[float] = None,
    original_function: Optional[Callable[[float], float]] = None
) -> None:
    x_min = min(xs)
    x_max = max(xs)
    margin = (x_max - x_min) * 0.15 if x_max > x_min else 1.0

    dense_x = [
        x_min - margin + i * (x_max - x_min + 2 * margin) / 500
        for i in range(501)
    ]

    lagrange_y = [lagrange_interpolation(xs, ys, xx) for xx in dense_x]
    newton_y = [newton_divided_interpolation(xs, ys, xx) for xx in dense_x]

    plt.figure(figsize=(10, 6))
    plt.scatter(xs, ys, label="Узлы интерполяции")

    if original_function is not None:
        original_y = [original_function(xx) for xx in dense_x]
        plt.plot(dense_x, original_y, label="Исходная функция")

    plt.plot(dense_x, lagrange_y, label="Лагранж")
    plt.plot(dense_x, newton_y, "--", label="Ньютон")

    if is_equally_spaced(xs):
        gauss_y = [gauss_interpolation_auto(xs, ys, xx)[0] for xx in dense_x]
        plt.plot(dense_x, gauss_y, ":", label="Гаусс")

    if x_query is not None:
        y_query = lagrange_interpolation(xs, ys, x_query)
        plt.scatter([x_query], [y_query], s=80, label=f"x = {x_query:.6f}")

    plt.title("Интерполяция функции")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def evaluate_methods(xs: List[float], ys: List[float], x_query: float) -> None:
    print(f"\nВычисление для x = {x_query:.6f}")

    y_lagrange = lagrange_interpolation(xs, ys, x_query)
    print(f"1. Лагранж:                    {y_lagrange:.10f}")

    y_newton = newton_divided_interpolation(xs, ys, x_query)
    print(f"2. Ньютон (разд. разности):   {y_newton:.10f}")

    if is_equally_spaced(xs):
        y_gauss, formula_name = gauss_interpolation_auto(xs, ys, x_query)
        print(f"4. {formula_name}:            {y_gauss:.10f}")

        print("\nСравнение результатов:")
        print(f"|Лагранж - Ньютон| = {abs(y_lagrange - y_newton):.12f}")
        print(f"|Лагранж - Гаусс|  = {abs(y_lagrange - y_gauss):.12f}")
        print(f"|Ньютон - Гаусс|   = {abs(y_newton - y_gauss):.12f}")
    else:
        print("4. Гаусс: нельзя применить, узлы не равноотстоящие.")



def main():
    while True:
        print("\n==============================")
        print("ЛР №5. Интерполяция функции")
        print("Вариант 12")
        print("==============================")
        print("1. Использовать готовые данные варианта 12")
        print("2. Ввести таблицу с клавиатуры")
        print("3. Считать таблицу из файла")
        print("4. Сформировать таблицу по функции")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        try:
            if choice == "1":
                xs, ys = get_variant_12_data()
                original_function = None
                print("\nЗагружены данные варианта 12.")
                print_source_table(xs, ys)
                print_finite_differences(xs, ys)
                pause()

            elif choice == "2":
                xs, ys, original_function = input_data_from_keyboard()
                print_source_table(xs, ys)
                print_finite_differences(xs, ys)
                pause()

            elif choice == "3":
                xs, ys, original_function = input_data_from_file()
                print_source_table(xs, ys)
                print_finite_differences(xs, ys)
                pause()

            elif choice == "4":
                xs, ys, original_function = choose_function_data()
                print_source_table(xs, ys)
                print_finite_differences(xs, ys)
                pause()

            elif choice == "0":
                print("Программа завершена.")
                break

            else:
                print("Некорректный выбор.")
                continue

            while True:
                print("\n------------------------------")
                print("Меню работы с текущими данными")
                print("------------------------------")
                print("1. Вычислить значение в заданной точке")
                print("2. Построить график")
                print("3. Показать X1 и X2 варианта 12")
                print("4. Показать исходную таблицу")
                print("5. Показать таблицу конечных разностей")
                print("6. Выбрать другой способ ввода данных")
                print("0. Выход")

                action = input("Ваш выбор: ").strip()

                if action == "1":
                    x_query = input_float("Введите x: ")
                    evaluate_methods(xs, ys, x_query)
                    pause()

                elif action == "2":
                    answer = input("Отметить точку x на графике? (y/n): ").strip().lower()
                    x_query = None
                    if answer == "y":
                        x_query = input_float("Введите x: ")
                    plot_interpolation(xs, ys, x_query, original_function)

                elif action == "3":
                    print("\nДля варианта 12:")
                    print("X1 = 0.523")
                    print("X2 = 0.639")
                    print("\nПроверка вычислений:")
                    evaluate_methods(xs, ys, 0.523)
                    evaluate_methods(xs, ys, 0.639)
                    pause()

                elif action == "4":
                    print_source_table(xs, ys)
                    pause()

                elif action == "5":
                    print_finite_differences(xs, ys)
                    pause()

                elif action == "6":
                    break

                elif action == "0":
                    print("Программа завершена.")
                    return

                else:
                    print("Некорректный выбор.")

        except Exception as exception:
            print(f"\nОшибка: {exception}")
            pause()


if __name__ == "__main__":
    main()