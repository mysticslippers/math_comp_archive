import matplotlib.pyplot as plt
import numpy as np


def system1(x):
    return np.array([
        -0.3 + 0.1 * x[0]**2 + x[0] + 0.2 * x[1]**2,
        0.2 * x[1]**2 + x[1] + 0.1 * x[0] * x[1] - 0.7
    ])


def phi1(x):
    return np.array([
        0.3 - 0.1 * x[0]**2 - 0.2 * x[1]**2,
        -0.2 * x[1]**2 - 0.1 * x[0] * x[1] + 0.7
    ])


def derivative_phi_system1(x):
    return np.array([
        [-0.2 * x[0], -0.4 * x[1]],
        [-0.4 * x[0] - 0.1 * x[1], -0.1 * x[0]]
    ])


def system2(x):
    return np.array([
        x[0] ** 2 + x[1] ** 2 - 4,
        x[0] - x[1] - 1
    ])


def phi2(x):
    return np.array([
        np.sqrt(4 - x[1]**2),
        x[0] - 1
    ])


def derivative_phi_system2(x):
    return np.array([
        [0, -x[1] / (np.sqrt(4 - x[1]**2))],
        [1, 0]
    ])


def list_systems():
    systems = [
        "1. Система 1:",
        "   0.1 * x[0]^2 + x[0] + 0.2 * x[1]^2 = 0.1",
        "   0.2 * x[1]^2 + x[1] + 0.1 * x[0] * x[1] = 0.2\n",
        "2. Система 2:",
        "   x^2 + y^2 = 4",
        "   x - y = 1"
    ]
    print("".join(systems))


def get_system(choice):
    systems = {
        1: system1,
        2: system2
    }

    phis = {
        1: phi1,
        2: phi2
    }

    derivative_systems = {
        1: derivative_phi_system1,
        2: derivative_phi_system2
    }
    return systems.get(choice, None), phis.get(choice, None), derivative_systems.get(choice, None)


def read_system_choice(prompt="Выберите систему уравнений: (1) первая система (2) вторая система: "):
    list_systems()

    while True:
        try:
            system_choice = int(input(prompt))
            if 1 <= system_choice <= 2:
                return system_choice
            else:
                print("Некорректный выбор функции! Попробуйте снова.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_initial_approximation(prompt="\nВведите начальные приближения x1, x2."):
    while True:
        try:
            print(prompt)
            x1 = round(float(input("Введите начальное приближение x1: ")), 2)
            x2 = round(float(input("Введите начальное приближение x2: ")), 2)
            initial_approximation = (x1, x2)
            return initial_approximation
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_tolerance(prompt="\nВведите допустимую погрешность (0 < tolerance <= 1): "):
    while True:
        try:
            tolerance = round(float(input(prompt)), 2)
            if 0 < tolerance <= 1:
                return tolerance
            else:
                print("Некорректный ввод! Пожалуйста, введите значение в диапазоне от 0 до 1.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_number_iterations(prompt="\nВведите максимальное количество итераций: "):
    while True:
        try:
            number_iterations = int(input(prompt))
            if 0 < number_iterations:
                return number_iterations
            else:
                print("Некорректный ввод! Пожалуйста, введите значение больше 0.")
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")


def read_input():
    system_choice = read_system_choice()
    x1, x2 = read_initial_approximation()
    initial_approximation = (x1, x2)
    tolerance = read_tolerance()
    iterations = read_number_iterations()
    return system_choice, initial_approximation, tolerance, iterations


def plot(system, initial_approximation, x1_range=(-2, 2), x2_range=(-2, 2), resolution=100):
    x1_values = np.linspace(x1_range[0], x1_range[1], resolution)
    x2_values = np.linspace(x2_range[0], x2_range[1], resolution)

    X1, X2 = np.meshgrid(x1_values, x2_values)
    Z1 = np.zeros_like(X1)
    Z2 = np.zeros_like(X2)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            x = np.array([X1[i, j], X2[i, j]])
            Z = system(x)
            Z1[i, j] = Z[0]
            Z2[i, j] = Z[1]

    plt.figure(figsize=(10, 6))
    plt.contour(X1, X2, Z1, levels=[0], colors='r', linewidths=2)
    plt.contour(X1, X2, Z2, levels=[0], colors='b', linewidths=2)
    plt.scatter(*initial_approximation, color='black', label='Начальное приближение', zorder=5)

    plt.title("График системы уравнений")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.axhline(0, color='grey', lw=0.5, ls='--')
    plt.axvline(0, color='grey', lw=0.5, ls='--')
    plt.grid()
    plt.legend()
    plt.show()


def check_convergence(system_derivative, x):
    q = np.max(np.abs((system_derivative(x))))
    print(f"Коэффициент сходимости q = {q}\n")
    if q >= 1:
        print("Система не удовлетворяет достаточному условию сходимости!")
        return False
    else:
        return True


def simple_iteration_system(system, phi, initial_approximation, tolerance, max_iterations):
    iterations = 0
    residuals = []
    x_current = initial_approximation

    for i in range(max_iterations):
        x_next = phi(x_current)
        print(x_next)

        residuals.append(system(x_next))

        diff_x0 = abs(x_next[0] - x_current[0])
        print(f"Разница между корнями x_0: {diff_x0}")
        diff_x1 = abs(x_next[1] - x_current[1])
        print(f"Разница между корнями x_1: {diff_x1}")

        maximum_diff = diff_x0 if diff_x0 > diff_x1 else diff_x1
        print(f"Разница между корнями: {maximum_diff}\n")

        system_next_value = system(x_next)
        if maximum_diff < tolerance and (abs(system_next_value[0])) < tolerance and (abs(system_next_value[1])) < tolerance:
            return x_next, iterations, residuals

        x_current = x_next
        iterations += 1

    print(x_current)
    return x_current, iterations, residuals


def solve_system_nonlinear_equations():
    print("\n\t\tЧисленное решение системы нелинейных уравнений")
    system_choice, initial_approximation, tolerance, iterations = read_input()
    system, phi, derivative_phi = get_system(system_choice)

    if check_convergence(derivative_phi, initial_approximation):
        solution, iterations, residuals = simple_iteration_system(system, phi, initial_approximation, tolerance, iterations)
        plot(system, solution)

        print(f"Решение: x1 = {solution[0]}, x2 = {solution[1]}")
        print(f"Количество итераций: {iterations}")
        print(f"Вектор погрешностей: {residuals}")

        residual = np.linalg.norm(phi(solution))
        print(f"Нормированное значение функции в найденной точке: {residual}")
