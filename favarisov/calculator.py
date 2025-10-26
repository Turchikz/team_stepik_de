def calculator():

    """Простой калькулятор основными операциями"""

    print("Добро пожаловать в калькулятор!")
    print("Доступные операции: +, -, *, /")

    try:
        num1 = float(input("Введите первое число: "))
        operator = input("Введите оператор (+, -, *, /): ")
        num2 = float(input("Введите второе число: "))
        
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                raise ZeroDivisionError("Ошибка: деление на ноль!")
            result = num1 / num2
        else:
            print("Неверный оператор!")
            return
            
        print(f"Результат: {num1} {operator} {num2} = {result}")
        
    except ValueError:
        print("Ошибка: введите корректные числа!")

    except ZeroDivisionError as e:
        print(e)

def run_calculator_with_retry():

    """Запускает калькулятор с возможностью повторного использования"""

    while True:
        calculator()

        again = input("\nХотите выполнить еще одно вычисление? (да/нет): ").lower()
        
        if again != 'да':
            print("Спасибо за использование калькулятора!")
            break