import string
from collections import Counter
import re

def text_analyzer(text):

    """Функция для анализа текста и вывода статистики"""
    
    # Проверка входных данных
    if not text or not text.strip():
        print("Ошибка: текст не может быть пустым!")
        return
    
    # Более точная очистка текста (учитываем разные пробельные символы)
    text_clean = text.translate(str.maketrans('', '', string.punctuation))

    # Используем регулярное выражение для разделения на слова
    words = re.findall(r'\b\w+\b', text_clean.lower())
    
    #Обработка ошибки в случае если нет слов для анализа 
    if not words:
        print("В тексте не найдено слов для анализа!")
        return
    
    # Основная статистика
    total_words = len(words) #Подсчет количества слов
    total_chars = len(text.replace(' ', '')) #Подсчет количества символов, без пробелов
    unique_words = len(set(words)) #Подсчет уникальных слов
    
    # Частотный анализ
    word_freq = Counter(words)
    common_words = word_freq.most_common(5)  # Увеличили до 5 самых частых слов
    
    # Анализ по длине слов
    word_lengths = [len(word) for word in words]
    avg_length = sum(word_lengths) / len(word_lengths) #Вычисляем среднюю длину слова
    
    # Дополнительная статистика
    lexical_diversity = unique_words / total_words * 100  # Лексическое разнообразие
    
    # Вывод результатов
    print()
    print("*" * 45)
    print()
    print("ПОДРОБНЫЙ АНАЛИЗ ТЕКСТА")
    print()
    print("*" * 45)
    print()
    print(f"📊 ОСНОВНАЯ СТАТИСТИКА:")
    print()
    print(f"   Общее количество слов: {total_words:,}")
    print(f"   Общее количество символов (без пробелов): {total_chars:,}")
    print(f"   Количество уникальных слов: {unique_words:,}")
    print(f"   Лексическое разнообразие представленного текста: {lexical_diversity:.1f}%")
    print()
    print("_" * 45)
    print()
    print(f"\n🏆 САМЫЕ ЧАСТЫЕ СЛОВА:")
    print()
    print("*" * 45)
    print()

    for i, (word, count) in enumerate(common_words, 1):
        percentage = (count / total_words) * 100
        print(f"   {i}. '{word}': {count} раз ({percentage:.1f}%)")
    
    print()
    print("_" * 45)
    print()
    print(f"\n📏 АНАЛИЗ ДЛИНЫ СЛОВ:")
    print()
    print("*" * 45)
    print()
    print(f"   Средняя длина слова: {avg_length:.1f} символов")
    print(f"   Самое длинное слово: '{max(words, key=len)}' ({len(max(words, key=len))} симв.)")
    print(f"   Самое короткое слово: '{min(words, key=len)}' ({len(min(words, key=len))} симв.)")
    print()

    # Распределение по длинам слов
    length_distribution = Counter(word_lengths)
    print()
    print("_" * 45)
    print()
    print(f"\n📈 РАСПРЕДЕЛЕНИЕ СЛОВ ПО ДЛИНЕ:")
    print()
    print("*" * 45)
    print()
    for length in sorted(length_distribution.keys()):
        count = length_distribution[length]
        percentage = (count / total_words) * 100
        bar = "█" * int(percentage / 2)  # Визуализация
        print(f"   {length:2} симв.: {count:3} слов {bar} ({percentage:.1f}%)")
    print()
    print("_" * 45)
    print()

# Пример использования
if __name__ == "__main__":
    sample_text = """
    Быстрая коричневая лиса прыгает через ленивую собаку. 
    Эта лиса очень быстрая и умная. Собака же предпочитает отдыхать.
    """
    
    text_analyzer(sample_text)