import numpy as np
import matplotlib.pyplot as plt


def find_optimal_intervals(sizes, percentages=[75, 80, 85, 90]):
    """
    Знаходить найвужчі проміжки, що містять задані відсотки файлів

    Параметри:
        sizes - відсортований список розмірів файлів
        percentages - список відсотків для аналізу

    Повертає:
        Словник з результатами для кожного відсотка
    """
    total_files = len(sizes)
    results = {}

    for percent in percentages:
        # Кількість файлів, що мають потрапити в проміжок
        target_count = int(total_files * percent / 100)
        min_range = float('inf')
        best_start = 0
        best_end = 0

        # Шукаємо найвужчий проміжок, що містить target_count файлів
        for i in range(total_files - target_count + 1):
            current_range = sizes[i + target_count - 1] - sizes[i]
            if current_range < min_range:
                min_range = current_range
                best_start = sizes[i]
                best_end = sizes[i + target_count - 1]

        # Зберігаємо результати
        results[percent] = {
            'start': best_start,
            'end': best_end,
            'range': min_range,
            'count': target_count,
            'actual_percent': (target_count / total_files) * 100
        }

    return results


def visualize_results(sizes, results):
    """Візуалізує результати на графіку"""
    plt.figure(figsize=(12, 6))

    # Побудова графіку розподілу
    counts, bins, _ = plt.hist(sizes, bins=100, alpha=0.5, color='blue', label='Розподіл файлів')

    # Додаємо проміжки на графік
    colors = ['red', 'green', 'purple', 'orange']
    for i, (percent, data) in enumerate(results.items()):
        plt.axvspan(data['start'], data['end'], alpha=0.2, color=colors[i],
                    label=f"{percent}% файлів: {data['start']}-{data['end']} байт")

    plt.xscale('log')
    plt.title('Найвужчі проміжки для різних відсотків файлів')
    plt.xlabel('Розмір файлу (байти, лог шкала)')
    plt.ylabel('Кількість файлів')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.show()


def main():
    # Зчитуємо дані з файлу
    try:
        with open("result.txt", 'r') as f:
            sizes = [int(line.strip()) for line in f if line.strip()]
        sizes.sort()
    except FileNotFoundError:
        print("Помилка: файл result.txt не знайдено")
        print("Спочатку виконайте команду для збору даних:")
        print(
            "find / -type f -not -path \"/proc/*\" -not -path \"/sys/*\" -not -path \"/dev/*\" -not -path \"/run/*\" -exec du -b {} + 2>/dev/null | awk '{print $1}' | sort -n > result.txt")
        return

    if not sizes:
        print("Файл result.txt порожній або містить некоректні дані")
        return

    # Аналізуємо дані
    percentages = [75, 80, 85, 90]
    results = find_optimal_intervals(sizes, percentages)

    # Виводимо результати
    print("\nРезультати аналізу:")
    print("-------------------")
    for percent, data in results.items():
        print(f"\n{percent}% файлів містяться в проміжку:")
        print(f"Від {data['start']} до {data['end']} байт")
        print(f"Ширина проміжку: {data['range']} байт")
        print(f"Фактичний відсоток: {data['actual_percent']:.2f}%")
        print(f"Кількість файлів: {data['count']} з {len(sizes)}")

    # Візуалізуємо результати
    visualize_results(sizes, results)


if __name__ == "__main__":
    main()