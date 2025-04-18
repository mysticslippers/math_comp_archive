import numpy as np


class NumericalIntegration:

    def __init__(self, function):
        self.function = function

    def left_rectangle(self, a, b, n):
        h = (b - a) / n
        total_area = 0
        for i in range(n):
            total_area += self.function(a + i * h)
        return total_area * h

    def right_rectangle(self, a, b, n):
        h = (b - a) / n
        total_area = 0
        for i in range(1, n + 1):
            total_area += self.function(a + i * h)
        return total_area * h

    def middle_rectangle(self, a, b, n):
        h = (b - a) / n
        total_area = 0
        for i in range(n):
            total_area += self.function(a + (i + 0.5) * h)
        return total_area * h

    def trapezoidal(self, a, b, n):
        h = (b - a) / n
        total_area = 0.5 * (self.function(a) + self.function(b))
        for i in range(1, n):
            total_area += self.function(a + i * h)
        return total_area * h

    def simpson(self, a, b, n):
        if n % 2 == 1:
            n += 1
        h = (b - a) / n
        total_area = self.function(a) + self.function(b)
        for i in range(1, n):
            if i % 2 == 0:
                total_area += 2 * self.function(a + i * h)
            else:
                total_area += 4 * self.function(a + i * h)
        return total_area * h / 3


def runge_error_estimation(val1, val2):
    return abs(val1 - val2) / 15


def main():
    print("Выберите функцию для интегрирования:")
    print("1. f(x) = x^2")
    print("2. f(x) = sin(x)")
    print("3. f(x) = e^x")
    print("4. f(x) = ln(x + 1)")
    print("5. f(x) = cos(x)")

    choice = int(input("Введите номер функции (1-5): "))
    if choice == 1:
        function = lambda x: x ** 2
    elif choice == 2:
        function = lambda x: np.sin(x)
    elif choice == 3:
        function = lambda x: np.exp(x)
    elif choice == 4:
        function = lambda x: np.log(x + 1)
    elif choice == 5:
        function = lambda x: np.cos(x)
    else:
        print("Некорректный выбор функции.")
        return

    a = float(input("Введите нижний предел интегрирования: "))
    b = float(input("Введите верхний предел интегрирования: "))
    target_error = float(input("Введите требуемую точность: "))

    integration_method = NumericalIntegration(function)
    n = 4
    error = float('inf')
    current_value = 0

    while error > target_error:
        last_value = current_value
        current_value = integration_method.simpson(a, b, n)
        if n > 4:
            error = runge_error_estimation(last_value, current_value)
        n *= 2

    print(f"Значение интеграла: {current_value}")
    print(f"Число разбиения для достижения требуемой точности: {n // 2}")


if __name__ == "__main__":
    main()
