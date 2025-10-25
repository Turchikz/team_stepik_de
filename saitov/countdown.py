import time


def countdown_timer(seconds):
    """Таймер обратного отсчёта"""
    while seconds:
        # Преобразуем секунды в формат MM:SS
        mins, secs = divmod(seconds, 60)
        timer_format = f"{mins:02d}:{secs:02d}"

        # Выводим время с возвратом каретки (\r)
        print(timer_format, end='\r')

        # Ждём 1 секунду
        time.sleep(1)

        # Уменьшаем счётчик
        seconds -= 1

    print("Время вышло! ⏰")


# Получаем время от пользователя
try:
    total_seconds = int(input("Введите время в секундах: "))
    countdown_timer(total_seconds)
except ValueError:
    print("Пожалуйста, введите целое число!")

# Конец кода Артура С.
