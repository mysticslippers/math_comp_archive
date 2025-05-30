# Лабораторная работа №4 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206


import csv
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

variable = sp.symbols('x')
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


def read_file(file_path=INPUT_FILE_PATH):
    try:
        dots = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                current_dot = tuple(map(float, row))
                dots.append(current_dot)
            return np.array(dots)
    except (ValueError, IndexError, FileNotFoundError) as exception:
        print(f"Ошибка при чтении файла: {exception}. Режим ввода переключён на консоль.")
        return None


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


def main():
    print("\t\t\t\t\t\tЛабораторная работа №4")
    

if __name__ == "__main__":
    main()
