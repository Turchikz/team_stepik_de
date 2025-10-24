import string
from collections import Counter


def text_analyzer(text):
    """Анализирует текст и выводит статистику"""

    # Убираем пунктуацию и приводим к нижнему регистру
    text_clean = text.translate(str.maketrans('', '', string.punctuation))
    words = text_clean.lower().split()

    # Статистика
    total_words = len(words)
    total_chars = len(text.replace(' ', ''))
    unique_words = len(set(words))

    # Самые частые слова
    word_freq = Counter(words)
    common_words = word_freq.most_common(3)

    # Вывод результатов
    print("=" * 40)
    print("АНАЛИЗ ТЕКСТА")
    print("=" * 40)
    print(f"Общее количество слов: {total_words}")
    print(f"Общее количество символов (без пробелов): {total_chars}")
    print(f"Уникальных слов: {unique_words}")
    print(f"\nСамые частые слова:")

    for word, count in common_words:
        print(f"  '{word}': {count} раз(а)")

    # Анализ по длине слов
    word_lengths = [len(word) for word in words]
    avg_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

    print(f"\nСредняя длина слова: {avg_length:.1f} символов")
    print(f"Самое длинное слово: {max(words, key=len) if words else 'N/A'}")
    print(f"Самое короткое слово: {min(words, key=len) if words else 'N/A'}")
