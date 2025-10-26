import time


def countdown_timer(seconds):

    """Создаем таймер обратного отсчёта"""

    while seconds:

        # Преобразуем секунды в формат MM:SS
        mins, secs = divmod(seconds, 60)
        timer_format = f"{mins:02d}:{secs:02d}"
        print(timer_format, end='\r') # Выводим время с возвратом каретки (\r)
        time.sleep(1) # Ждём 1 секунду
        seconds -= 1 # Уменьшаем счётчик

    print("Время вышло! ⏰")


# Получаем время от пользователя
try:
    total_seconds = int(input("Введите время в секундах: "))

    countdown_timer(total_seconds)

except ValueError:

    print("Пожалуйста, введите целое число!")

### Конец кода Артура С.
