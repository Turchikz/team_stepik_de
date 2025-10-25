import time
import keyboard  # нужно установить: pip install keyboard


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.paused = False
        self.pause_time = 0
        self.total_pause_time = 0

    def start(self):
        """Запуск секундомера"""
        if self.start_time is None:
            self.start_time = time.time()
            print("Секундомер запущен!")
        elif self.paused:
            self.total_pause_time += time.time() - self.pause_time
            self.paused = False
            print("Тик-Так. Секундомер возобновлён!")
        else:
            print("Тик-Так. Секундомер уже запущен!")

    def pause(self):
        """Пауза секундомера"""
        if self.start_time is not None and not self.paused:
            self.pause_time = time.time()
            self.paused = True
            print("Секундомер на паузе!")
        elif self.paused:
            print("Секундомер уже на паузе!")
        else:
            print("Секундомер ещё не запущен!")

    def stop(self):
        """Остановка и сброс секундомера"""
        if self.start_time is not None:
            elapsed = self.get_elapsed_time()
            self.start_time = None
            self.paused = False
            self.total_pause_time = 0
            print(
                f"Секундомер остановлен. Общее время: {self.format_time_with_ms(elapsed)}")
            return elapsed
        else:
            print("Секундомер ещё не запущен!")
            return 0

    def get_elapsed_time(self):
        """Получить прошедшее время"""
        if self.start_time is None:
            return 0

        if self.paused:
            return self.pause_time - self.start_time - self.total_pause_time
        else:
            return time.time() - self.start_time - self.total_pause_time

    def display_time(self):
        """Отобразить текущее время в формате HH:MM:SS"""
        elapsed = self.get_elapsed_time()
        return self.format_time(elapsed)

    def format_time(self, seconds):
        """Форматирует время в секундах в строку HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds_int = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds_int:02d}"

    # ИЗМЕНЕНИЕ: Добавление метода для отображения времени с миллисекундами
    def format_time_with_ms(self, seconds):
        """Форматирует время в секундах в строку HH:MM:SS.mmm с миллисекундами"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds_int = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)  # Получаем миллисекунды
        return f"{hours:02d}:{minutes:02d}:{seconds_int:02d}.{milliseconds:03d}"

    def display_time_with_ms(self):
        """Отобразить текущее время в формате HH:MM:SS.mmm с миллисекундами"""
        elapsed = self.get_elapsed_time()
        return self.format_time_with_ms(elapsed)


def simple_stopwatch():
    """Простая версия секундомера без паузы"""
    input("Нажмите Enter для запуска секундомера...")
    start_time = time.time()
    print("Секундомер запущен! Нажмите Ctrl+C для остановки.")

    try:
        while True:
            elapsed = time.time() - start_time
            # ИЗМЕНЕНИЕ: Добавляем миллисекунды в отображение
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            milliseconds = int((elapsed % 1) * 1000)  # Получаем миллисекунды
            print(
                f"\rПрошло времени: {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}", end="")
            # Уменьшаем задержку для плавного отображения миллисекунд
            time.sleep(0.01)
    except KeyboardInterrupt:
        end_time = time.time()
        total_time = end_time - start_time
        # ИЗМЕНЕНИЕ: Выводим итоговое время с миллисекундами
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        milliseconds = int((total_time % 1) * 1000)
        print(
            f"\n\nОбщее время: {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")


def interactive_stopwatch():
    """Интерактивный секундомер с управлением"""
    stopwatch = Stopwatch()

    print("🎯 ИНТЕРАКТИВНЫЙ СЕКУНДОМЕР 🎯")
    print("=" * 40)
    print("Управление:")
    print("1 - Старт/Продолжить")
    print("2 - Пауза")
    print("3 - Стоп/Сброс")
    print("0 - Выход")
    print("=" * 40)

    try:
        while True:
            if stopwatch.start_time is not None and not stopwatch.paused:
                # ИЗМЕНЕНИЕ: Используем отображение с миллисекундами
                print(
                    f"\rТекущее время: {stopwatch.display_time_with_ms()}", end="")

            # Ждём ввод пользователя
            choice = input("\n\nВыберите действие (1/2/3/0): ").strip()

            if choice == "1":
                stopwatch.start()
            elif choice == "2":
                stopwatch.pause()
                if stopwatch.paused:
                    # ИЗМЕНЕНИЕ: Выводим время на паузе с миллисекундами
                    print(
                        f"Время на паузе: {stopwatch.display_time_with_ms()}")
            elif choice == "3":
                elapsed = stopwatch.stop()
                if elapsed > 0:
                    # ИЗМЕНЕНИЕ: Выводим зафиксированное время с миллисекундами
                    print(
                        f"Зафиксированное время: {stopwatch.display_time_with_ms()}")
            elif choice == "0":
                print("Выход из секундомера.")
                break
            else:
                print("Неверный выбор! Используйте 1, 2, 3 или 0.")

    except KeyboardInterrupt:
        print("\n\nСекундомер завершён!")


if __name__ == "__main__":
    print("Выберите режим секундомера:")
    print("1 - Простой секундомер")
    print("2 - Интерактивный секундомер")

    choice = input("Ваш выбор (1/2): ").strip()

    if choice == "1":
        simple_stopwatch()
    elif choice == "2":
        interactive_stopwatch()
    else:
        print("Неверный выбор! Запускаю простой режим...")
        simple_stopwatch()
