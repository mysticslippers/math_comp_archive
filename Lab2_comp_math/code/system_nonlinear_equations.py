import matplotlib.pyplot as plt
import numpy as np


def system1(x):
    return np.array([
        np.sin(x[0]) + x[1] - 1,
        np.cos(x[1]) + x[0] - 1
    ])


def phi1(x):
    return np.array([
        np.arcsin(1 - x[1]),
        np.arccos(1 - x[0])
    ])


def derivative_system1(x):
    return np.array([
        [-1 / (np.sqrt(2 * x[1] - x[1]^2)), 0],
        [0, -1 / np.sqrt(2 - x[0])]
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


def derivative_system2(x):
    return np.array([
        [0, -x[0] / (np.sqrt(4 - x[0]**2))],
        [1, 0]
    ])


def list_systems():
    systems = [
        "1. Система 1:",
        "   sin(x) + y = 1",
        "   cos(y) + x = 1\n",
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
        1: derivative_system1,
        2: derivative_system2
    }
    return systems.get(choice, None), phis.get(choice, None), derivative_systems.get(choice, None)


def read_system_choice(prompt="Выберите систему уравнений: (1) первая система (2) вторая система"):
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


def read_borders():
    while True:
        try:
            a = float(input("Введите левую границу интервала (a): "))
            b = float(input("Введите правую границу интервала (b): "))
            return a, b

        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовые значения.")
