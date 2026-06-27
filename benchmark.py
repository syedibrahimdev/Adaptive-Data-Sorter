import random
import time
import matplotlib.pyplot as plt
from AdaptiveSSS import AdaptiveSortingSearchingSystem, CompositeKey


def generate_random_data(n):
    names = ["Ibrahim", "Muzammil", "Hamza", "Sudais", "Aoun"]
    return [CompositeKey(random.randint(1, n * 2), random.choice(names)) for _ in range(n)]


def generate_nearly_sorted_data(n):
    data = sorted(generate_random_data(n), key=lambda x: (x.id, x.name))
    # Shuffle ~5% of elements to simulate "nearly sorted"
    swaps = max(1, n // 20)
    for _ in range(swaps):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        data[i], data[j] = data[j], data[i]
    return data


def time_pure_algorithm(data, algo_name):
    """Time a single algorithm directly, bypassing auto-selection, for fair comparison."""
    system = AdaptiveSortingSearchingSystem('composite')
    system.data = data.copy()

    start = time.time()
    if algo_name == 'insertion':
        system._insertion_sort()
    elif algo_name == 'merge':
        system._merge_sort()
    elif algo_name == 'builtin':
        system.data.sort(key=lambda x: (x.id, x.name))
    return time.time() - start


def run_benchmark():
    sizes = [100, 500, 1000, 5000, 10000]
    results = {'insertion': [], 'merge': [], 'builtin': []}

    for n in sizes:
        print(f"Benchmarking n={n}...")
        random_data = generate_random_data(n)
        for algo in results:
            elapsed = time_pure_algorithm(random_data, algo)
            results[algo].append(elapsed)

    plt.figure(figsize=(9, 6))
    for algo, times in results.items():
        plt.plot(sizes, times, marker='o', label=algo.capitalize())

    plt.title('Sorting Algorithm Performance on Random Data', fontsize=14)
    plt.xlabel('Number of Records')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('images/benchmark_random.png')
    plt.show()


def run_nearly_sorted_benchmark():
    sizes = [100, 500, 1000, 5000, 10000]
    results = {'insertion': [], 'merge': []}

    for n in sizes:
        print(f"Benchmarking nearly-sorted n={n}...")
        data = generate_nearly_sorted_data(n)
        for algo in results:
            elapsed = time_pure_algorithm(data, algo)
            results[algo].append(elapsed)

    plt.figure(figsize=(9, 6))
    for algo, times in results.items():
        plt.plot(sizes, times, marker='o', label=algo.capitalize())

    plt.title('Insertion vs Merge Sort on Nearly-Sorted Data', fontsize=14)
    plt.xlabel('Number of Records')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('images/benchmark_nearly_sorted.png')
    plt.show()


if __name__ == "__main__":
    import os
    os.makedirs('images', exist_ok=True)
    run_benchmark()
    run_nearly_sorted_benchmark()