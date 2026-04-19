import math
from typing import Callable, List

import matplotlib.pyplot as plt


def f1(x: float, y: float) -> float:
    return y + (1 + x) * y * y


def exact1(x: float, x0: float, y0: float) -> float:
    if abs(y0) < 1e-14:
        raise ValueError("Для уравнения 1 при y0 = 0 точное решение в этой формуле не определяется.")
    c = math.exp(x0) * (x0 + 1.0 / y0)
    denom = c * math.exp(-x) - x
    if abs(denom) < 1e-14:
        raise ValueError(f"Точное решение уравнения 1 имеет разрыв при x = {x:.6f}.")
    return 1.0 / denom


def f2(x: float, y: float) -> float:
    return x * x - 2 * y


def exact2(x: float, x0: float, y0: float) -> float:
    c = (y0 - (x0 * x0 / 2.0 - x0 / 2.0 + 0.25)) * math.exp(2 * x0)
    return x * x / 2.0 - x / 2.0 + 0.25 + c * math.exp(-2 * x)


def f3(x: float, y: float) -> float:
    return x + y


def exact3(x: float, x0: float, y0: float) -> float:
    c = (y0 + x0 + 1.0) / math.exp(x0)
    return c * math.exp(x) - x - 1.0


ODES = {
    1: {
        "name": "y' = y + (1 + x) y^2",
        "f": f1,
        "exact": exact1
    },
    2: {
        "name": "y' = x^2 - 2y",
        "f": f2,
        "exact": exact2
    },
    3: {
        "name": "y' = x + y",
        "f": f3,
        "exact": exact3
    }
}


def read_int(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            print(f"Введите целое число от {min_value} до {max_value}.")
        except ValueError:
            print("Ошибка: нужно ввести целое число.")


def read_float(prompt: str, positive: bool = False) -> float | None:
    while True:
        try:
            value = float(input(prompt))
            if positive and value <= 0:
                print("Число должно быть больше 0.")
                continue
            return value
        except ValueError:
            print("Ошибка: нужно ввести число.")


def build_grid(x0: float, xn: float, h: float) -> List[float]:
    if xn <= x0:
        raise ValueError("Правая граница должна быть больше левой.")
    if h <= 0:
        raise ValueError("Шаг h должен быть больше 0.")

    length = xn - x0
    n = int(round(length / h))

    if n <= 0:
        raise ValueError("Слишком большой шаг: на интервале нет узлов.")

    if abs(x0 + n * h - xn) > 1e-10:
        raise ValueError(
            "Шаг h должен делить интервал [x0, xn] без остатка.\n"
            "Например, для [0, 1] подойдут h = 0.1, 0.2, 0.25 и т.д."
        )

    return [x0 + i * h for i in range(n + 1)]


def max_abs_diff(a: List[float], b: List[float]) -> float:
    return max(abs(x - y) for x, y in zip(a, b))


def runge_error(y_h: List[float], y_h2: List[float], p: int) -> List[float]:
    result = []
    for i in range(len(y_h)):
        y_half = y_h2[2 * i]
        result.append(abs(y_half - y_h[i]) / (2 ** p - 1))
    return result


def print_table(
    xs: List[float],
    y_exact: List[float],
    y_euler: List[float],
    y_rk4: List[float],
    y_milne: List[float],
    euler_runge: List[float],
    rk4_runge: List[float]
) -> None:
    header = (
        f"{'i':>3} {'x':>10} {'y_exact':>16} "
        f"{'Euler':>16} {'|e|':>12} {'Runge':>12} "
        f"{'RK4':>16} {'|e|':>12} {'Runge':>12} "
        f"{'Milne':>16} {'|e|':>12}"
    )
    print("\n" + header)
    print("-" * len(header))

    for i in range(len(xs)):
        e_err = abs(y_exact[i] - y_euler[i])
        rk_err = abs(y_exact[i] - y_rk4[i])
        m_err = abs(y_exact[i] - y_milne[i])

        print(
            f"{i:>3} {xs[i]:>10.5f} {y_exact[i]:>16.8f} "
            f"{y_euler[i]:>16.8f} {e_err:>12.3e} {euler_runge[i]:>12.3e} "
            f"{y_rk4[i]:>16.8f} {rk_err:>12.3e} {rk4_runge[i]:>12.3e} "
            f"{y_milne[i]:>16.8f} {m_err:>12.3e}"
        )


def euler_method(f: Callable[[float, float], float], xs: List[float], y0: float) -> List[float]:
    ys = [y0]
    for i in range(len(xs) - 1):
        h = xs[i + 1] - xs[i]
        y_next = ys[i] + h * f(xs[i], ys[i])
        ys.append(y_next)
    return ys


def rk4_method(f: Callable[[float, float], float], xs: List[float], y0: float) -> List[float]:
    ys = [y0]
    for i in range(len(xs) - 1):
        x = xs[i]
        y = ys[i]
        h = xs[i + 1] - xs[i]

        k1 = h * f(x, y)
        k2 = h * f(x + h / 2.0, y + k1 / 2.0)
        k3 = h * f(x + h / 2.0, y + k2 / 2.0)
        k4 = h * f(x + h, y + k3)

        y_next = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        ys.append(y_next)
    return ys


def milne_method(
    f: Callable[[float, float], float],
    xs: List[float],
    y0: float,
    eps: float
) -> List[float]:
    n = len(xs) - 1
    if n < 3:
        raise ValueError("Для метода Милна нужно минимум 4 точки сетки (хотя бы 3 шага).")

    start_xs = xs[:4]
    ys = rk4_method(f, start_xs, y0)

    for i in range(3, n):
        h = xs[i + 1] - xs[i]

        f_im2 = f(xs[i - 2], ys[i - 2])
        f_im1 = f(xs[i - 1], ys[i - 1])
        f_i = f(xs[i], ys[i])

        y_pred = ys[i - 3] + (4.0 * h / 3.0) * (2.0 * f_im2 - f_im1 + 2.0 * f_i)

        y_corr_prev = y_pred

        while True:
            f_pred = f(xs[i + 1], y_corr_prev)
            y_corr = ys[i - 1] + (h / 3.0) * (f_im1 + 4.0 * f_i + f_pred)

            if abs(y_corr - y_corr_prev) < eps:
                ys.append(y_corr)
                break

            y_corr_prev = y_corr

    return ys


def plot_solutions(
    xs: List[float],
    y_exact: List[float],
    y_euler: List[float],
    y_rk4: List[float],
    y_milne: List[float],
    equation_name: str
) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(xs, y_exact, label="Точное решение", linewidth=2)
    plt.plot(xs, y_euler, "o--", label="Эйлер")
    plt.plot(xs, y_rk4, "s--", label="Рунге-Кутта 4")
    plt.plot(xs, y_milne, "d--", label="Милн")

    plt.title(f"Численное решение ОДУ\n{equation_name}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main() -> None:
    print("Лабораторная работа №6")
    print("Вариант 12: Метод Эйлера, Рунге-Кутта 4-го порядка, Милна\n")

    print("Доступные уравнения:")
    for key, value in ODES.items():
        print(f"{key}. {value['name']}")

    choice = read_int("\nВыберите номер уравнения (1-3): ", 1, 3)
    x0 = read_float("Введите x0: ")
    xn = read_float("Введите xn (xn > x0): ")
    y0 = read_float("Введите y(x0): ")
    h = read_float("Введите шаг h: ", positive=True)
    eps = read_float("Введите точность eps: ", positive=True)

    try:
        xs = build_grid(x0, xn, h)
        ode = ODES[choice]
        f = ode["f"]
        exact = ode["exact"]

        y_exact = [exact(x, x0, y0) for x in xs]

        y_euler = euler_method(f, xs, y0)
        y_rk4 = rk4_method(f, xs, y0)
        y_milne = milne_method(f, xs, y0, eps)

        xs_half = build_grid(x0, xn, h / 2.0)
        y_euler_half = euler_method(f, xs_half, y0)
        y_rk4_half = rk4_method(f, xs_half, y0)

        euler_runge = runge_error(y_euler, y_euler_half, p=1)
        rk4_runge = runge_error(y_rk4, y_rk4_half, p=4)

        print_table(xs, y_exact, y_euler, y_rk4, y_milne, euler_runge, rk4_runge)

        print("\nМаксимальные ошибки:")
        print(f"Метод Эйлера:       {max_abs_diff(y_exact, y_euler):.6e}")
        print(f"Метод Рунге-Кутта:  {max_abs_diff(y_exact, y_rk4):.6e}")
        print(f"Метод Милна:        {max_abs_diff(y_exact, y_milne):.6e}")

        print("\nМаксимальные оценки по правилу Рунге:")
        print(f"Эйлер:              {max(euler_runge):.6e}")
        print(f"Рунге-Кутта 4:      {max(rk4_runge):.6e}")

        plot_solutions(xs, y_exact, y_euler, y_rk4, y_milne, ode["name"])

    except Exception as exception:
        print(f"\nОшибка: {exception}")


if __name__ == "__main__":
    main()