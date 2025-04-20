# Лабораторная работа №1 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

import numpy as np

FILE_PATH = "iofiles/input.txt"


def get_matrix_file():
    """ Получить матрицу из файла """
    try:
        with open(FILE_PATH, 'rt') as fin:
            n = int(fin.readline().strip())
            matrix = [list(map(float, line.strip().split())) for line in fin]

            if len(matrix) != n or any(len(row) != n + 1 for row in matrix):
                raise ValueError("Неверный размер матрицы!!")
    except (ValueError, FileNotFoundError, OSError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

    return matrix


def get_matrix_console():
    """ Получить матрицу с клавиатуры """
    print("Вводите коэффициенты матрицы через пробел строка за строкой.")

    n = get_matrix_order()
    if n is None:
        return None

    matrix = []
    print("Коэффициенты матрицы:")

    for i in range(n):
        while True:
            try:
                row = list(map(float, input(f"Введите строку {i + 1}: ").strip().split()))
                if len(row) != n + 1:
                    raise ValueError(f"Строка должна содержать {n + 1} элементов!")
                matrix.append(row)
                break
            except ValueError as ve:
                print(ve)

    return matrix


def print_matrix(matrix):
    """Выводит матрицу с форматированием."""
    for row in matrix:
        print(' '.join('{:10}'.format(round(col, 3)) for col in row))


def print_vector(vector):
    """Выводит вектор неизвестных с форматированием."""
    for value in vector:
        print('  ' + str(value))


def get_matrix_order():
    """Получить порядок матрицы от пользователя."""
    while True:
        try:
            n = int(input("Порядок матрицы: "))
            if n <= 0:
                print("Порядок матрицы должен быть положительным!")
            else:
                return n
        except ValueError:
            print("Порядок матрицы должен быть целым числом!")


def solve_gauss_method(matrix):
    """Решить СЛАУ методом Гаусса с выбором главного элемента."""
    swap_counter = 0
    size = len(matrix)

    for i in range(size - 1):
        max_row = i
        max_val = abs(matrix[i][i])

        for k in range(i + 1, size):
            current_val = abs(matrix[k][i])
            if current_val > max_val:
                max_val, max_row = current_val, k

        if max_row != i:
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            swap_counter += 1

        print(f"\nКоличество перестановок на {i}-м" + " шаге: " + str(swap_counter))
        if matrix[i][i] == 0:
            return 0


        for k in range(i + 1, size):
            factor = matrix[k][i] / matrix[i][i]
            for j in range(i, size + 1):
                matrix[k][j] -= factor * matrix[i][j]

            print(f"После изменения строки {k}:")
            print_matrix(matrix)

    roots = [0] * size
    for i in range(size - 1, -1, -1):
        s_part = sum(matrix[i][j] * roots[j] for j in range(i + 1, size))
        roots[i] = (matrix[i][size] - s_part) / matrix[i][i]

    residuals = [sum(matrix[i][j] * roots[j] for j in range(size)) - matrix[i][size] for i in range(size)]

    determinant = (-1) ** swap_counter
    for i in range(size):
        determinant *= matrix[i][i]

    return None if determinant == 0 else determinant, matrix, roots, residuals


def main():
    print("\t\tМетод Гаусса с выбором главного элемента по столбцам")
    method = input("\nВзять коэффициенты из файла или ввести с клавиатуры? (+/-)\n>>> ")

    while method not in ('+', '-'):
        print("Введите '+' или '-' для выбора способа ввода.")
        method = input(">>> ")

    matrix = get_matrix_file() if method == '+' else get_matrix_console()

    if matrix is None:
        print("При считывании коэффициентов матрицы произошла ошибка!")
        return

    answer = solve_gauss_method(matrix[:])
    if answer is None:
        print("\nМатрица является несовместной.")
        return

    determinant, reduced_matrix, roots, residuals = answer

    arr = np.array(matrix)
    square_dim = min(arr.shape)
    np_matrix = arr[:square_dim, :square_dim]
    np_determinant = np.linalg.det(np_matrix)

    print("\nОпределитель:")
    print(determinant)
    print("\nОпределитель при использовании библиотеки numpy:")
    print(np_determinant)

    print("\nПреобразованная матрица:")
    print_matrix(reduced_matrix)

    print("\nВектор неизвестных:")
    print_vector(roots)

    np_roots = np.linalg.solve(arr[:, :-1], arr[:, -1])
    print("\nВектор неизвестных при использовании библиотеки numpy:")
    print_vector(np_roots)

    print("\nВектор невязок:")
    print_vector(residuals)

    input("\n\nНажмите Enter, чтобы выйти.")


main()
