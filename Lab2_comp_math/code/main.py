# Лабораторная работа №2 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

from nonlinear_equation import solve_nonlinear_equation
from system_nonlinear_equations import solve_system_nonlinear_equations


def main():
    print("\t\tЛабораторная работа №2")
    while True:
        try:
            choice = input("Вы хотите решить 'нелинейное уравнение'/'систему нелинейных уравнений' (+/-): ").strip()
            if choice == '+':
                solve_nonlinear_equation()
                break
            elif choice == '-':
                solve_system_nonlinear_equations()
                break
            else:
                print("Неверный выбор. Пожалуйста, введите '+' для нелинейного уравнения или '-' для системы.")
        except Exception as e:
            print(f"Произошла ошибка: {e}. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
