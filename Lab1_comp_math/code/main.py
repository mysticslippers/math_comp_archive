# Лабораторная работа №1 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

import numpy as np

FILE_PATH = "iofiles/input.txt"


def readFile():
    """ Получить матрицу из файла """
    with open(FILE_PATH, 'rt') as fin:
        try:
            n = int(fin.readline())
            matrix = []
            for line in fin:
                new_row = list(map(float, line.strip().split()))
                if len(new_row) != (n + 1):
                    raise ValueError
                matrix.append(new_row)
            if len(matrix) != n:
                raise ValueError
        except ValueError:
            return None
    return matrix


def readConsole():
    """ Получить матрицу с клавиатуры """
    print("Вводите коэффициенты матрицы через пробел строка за строкой.")
    while True:
        try:
            n = int(input("Порядок матрицы: "))
            if n <= 0:
                print("Порядок матрицы должен быть положительным.")
            else:
                break
        except ValueError:
            print("Порядок матрицы должен быть целым числом.")
    matrix = []
    print("Коэффициенты матрицы:")
    try:
        for i in range(n):
            matrix.append(list(map(float, input().strip().split())))
            if len(matrix[i]) != (n + 1):
                raise ValueError
    except ValueError:
        return None
    return matrix


def solveMinor(matrix, i, j):
    """ Найти минор элемента матрицы """
    n = len(matrix)
    return [[matrix[row][col] for col in range(n) if col != j] for row in range(n) if row != i]


def solveDet(matrix):
    """ Найти определитель матрицы """
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sgn = 1
    for j in range(n):
        det += sgn * matrix[0][j] * solveDet(solveMinor(matrix, 0, j))
        sgn *= -1
    return det


def solve(matrix):
    """ Метод Гаусса с выбором главного элемента по столбцам """
    n = len(matrix)
    det = solveDet([matrix[i][:n] for i in range(n)])
    if det == 0:
        return None

    # Прямой ход
    for i in range(n - 1):
        # Поиск максимального элемента в столбце
        max_i = i
        for m in range(i + 1, n):
            if abs(matrix[m][i]) > abs(matrix[max_i][i]):
                max_i = m

        # Перестановка строк
        if max_i != i:
            for j in range(n + 1):
                matrix[i][j], matrix[max_i][j] = matrix[max_i][j], matrix[i][j]

        # Исключение i-того неизвестного
        for k in range(i + 1, n):
            coef = matrix[k][i] / matrix[i][i]
            for j in range(i, n + 1):
                matrix[k][j] -= coef * matrix[i][j]

    reduced_matrix = matrix[:]

    # Обратный ход
    roots = [0] * n
    for i in range(n - 1, -1, -1):
        s_part = 0
        for j in range(i + 1, n):
            s_part += matrix[i][j] * roots[j]
        roots[i] = (matrix[i][n] - s_part) / matrix[i][i]

    # Вычисление невязок
    residuals = [0] * n
    for i in range(n):
        s_part = 0
        for j in range(n):
            s_part += matrix[i][j] * roots[j]
        residuals[i] = s_part - matrix[i][n]

    return det, reduced_matrix, roots, residuals


def main():
    print("\t\tМетод Гаусса с выбором главного элемента по столбцам")
    print("\nВзять коэффициенты из файла или ввести с клавиатуры? (+/-)")

    method = input(">>> ")
    while (method != '+') and (method != '-'):
        print("Введите '+' или '-' для выбора способа ввода.")
        method = input(">>> ")

    if method == '+':
        matrix = readFile()
    else:
        matrix = readConsole()

    if matrix is None:
        print("При считывании коэффициентов матрицы произошла ошибка!")
        return

    answer = solve(matrix[:])
    if answer is None:
        print("\nМатрица является несовместной.")
        return
    det, reduced_matrix, roots, residuals = answer

    arr = np.array(matrix)
    square_counter = min(arr.shape)
    np_matrix = arr[:square_counter, :square_counter]
    np_det = np.linalg.det(np_matrix)
    print("\nОпределитель:")
    print(det)
    print("\nОпределитель при использовании библиотеки numpy:")
    print(np_det)

    print("\nПреобразованная матрица:")
    for row in reduced_matrix:
        for col in row:
            print('{:10}'.format(round(col, 3)), end='')
        print()

    print("\nВектор неизвестных:")
    for root in roots:
        print('  ' + str(root))

    np_roots = np.linalg.solve(arr[:, :-1], arr[:, -1])
    print("\nВектор неизвестных при использовании библиотеки numpy:")
    for root in np_roots:
        print('  ' + str(root))

    print("\nВектор невязок:")
    for residual in residuals:
        print('  ' + str(residual))

    input("\n\nНажмите Enter, чтобы выйти.")


main()
