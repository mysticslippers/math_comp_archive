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
