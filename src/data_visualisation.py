import matplotlib.pyplot as plt
import numpy as np


def read_file_sizes(filename):
    """Читає розміри файлів з файлу"""
    with open("result.txt", 'r') as f:
        sizes = [int(line.strip()) for line in f if line.strip()]
    return sorted(sizes)


def plot_file_distributions(sizes):
    """Створює всі необхідні діаграми"""
    if not sizes:
        print("Немає даних для візуалізації")
        return

    total_files = len(sizes)
    print(f"Всього файлів: {total_files}")

    # Підготовка даних для графіків
    unique_sizes, counts = np.unique(sizes, return_counts=True)

    # Кумулятивний розподіл
    cumul_percent = np.cumsum(counts) / total_files * 100

    # 1. Загальний розподіл (лог шкала)
    plt.figure(figsize=(12, 6))
    plt.scatter(unique_sizes, counts, s=5, alpha=0.5)
    plt.xscale('log')
    plt.title('Розподіл кількості файлів за розміром (лог шкала)')
    plt.xlabel('Розмір файлу (байти)')
    plt.ylabel('Кількість файлів')
    plt.grid(True, which="both", ls="--")
    plt.show()

    # 2. Кумулятивний розподіл (лог шкала)
    plt.figure(figsize=(12, 6))
    plt.plot(unique_sizes, cumul_percent)
    plt.xscale('log')
    plt.title('Відсоток файлів з розміром ≤ заданого (лог шкала)')
    plt.xlabel('Розмір файлу (байти)')
    plt.ylabel('Відсоток файлів (%)')
    plt.grid(True, which="both", ls="--")
    plt.show()

    # 3. Розподіл для малих файлів (0-1000 байт)
    small_sizes = [s for s in sizes if s <= 1000]
    if small_sizes:
        plt.figure(figsize=(12, 6))
        plt.hist(small_sizes, bins=50, edgecolor='black')
        plt.title('Розподіл файлів розміром 0-1000 байт')
        plt.xlabel('Розмір файлу (байти)')
        plt.ylabel('Кількість файлів')
        plt.grid(True)
        plt.show()

    # 4. Розподіл для середніх файлів (1000-1000000 байт)
    medium_sizes = [s for s in sizes if 1000 < s <= 1000000]
    if medium_sizes:
        plt.figure(figsize=(12, 6))
        plt.hist(medium_sizes, bins=50, edgecolor='black')
        plt.title('Розподіл файлів розміром 1000-1000000 байт')
        plt.xlabel('Розмір файлу (байти)')
        plt.ylabel('Кількість файлів')
        plt.grid(True)
        plt.show()

    # 5. Розподіл для великих файлів (>1000000 байт)
    large_sizes = [s for s in sizes if s > 1000000]
    if large_sizes:
        plt.figure(figsize=(12, 6))
        plt.hist(large_sizes, bins=20, edgecolor='black')
        plt.title('Розподіл файлів розміром >1000000 байт')
        plt.xlabel('Розмір файлу (байти)')
        plt.ylabel('Кількість файлів')
        plt.grid(True)
        plt.show()


def main():
    # Вхідний файл з розмірами
    input_file = 'result.txt'

    try:
        # Читаємо дані
        file_sizes = read_file_sizes(input_file)

        # Створюємо графіки
        plot_file_distributions(file_sizes)

    except FileNotFoundError:
        print(f"Файл {input_file} не знайдено. Спочатку виконайте команду:")
        print(
            "find / -type f -not -path \"/proc/*\" -not -path \"/sys/*\" -not -path \"/dev/*\" -not -path \"/run/*\" -exec du -b {} + 2>/dev/null | awk '{print $1}' | sort -n > result.txt")
    except Exception as e:
        print(f"Сталася помилка: {e}")


if __name__ == "__main__":
    main()

