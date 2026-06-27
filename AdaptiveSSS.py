import random
import time
from dataclasses import dataclass


@dataclass(order=True)
class CompositeKey:
    id: int
    name: str

    def __str__(self):
        return f"({self.id}, {self.name})"


class AdaptiveSortingSearchingSystem:
    """
    A sorting/searching system that picks the best algorithm automatically
    based on data size and how close the data already is to being sorted.

    Strategy:
    - Already sorted          -> skip sorting entirely (O(n) check, O(1) sort)
    - Small dataset (<= 50)   -> Insertion Sort (low overhead, fast on small n)
    - Nearly sorted           -> Insertion Sort (adaptive: O(n) best case)
    - Large, unsorted dataset -> Merge Sort (stable O(n log n) worst case)
    """

    SMALL_DATASET_THRESHOLD = 50
    NEARLY_SORTED_INVERSION_RATIO = 0.1  # <=10% out-of-place elements

    def __init__(self, key_type):
        self.key_type = key_type
        self.data = []
        self.last_algorithm_used = None

    def insert(self, item):
        self.data.append(item)

    def delete(self, item):
        if item in self.data:
            self.data.remove(item)

    def print_data(self):
        for item in self.data:
            print(item)

    def is_sorted(self):
        return all(self.data[i] <= self.data[i + 1] for i in range(len(self.data) - 1))

    def _count_inversions_sample(self, sample_size=200):
        """
        Estimate how 'unsorted' the data is by sampling adjacent-pair
        inversions, instead of checking every element (expensive on large n).
        """
        n = len(self.data)
        if n < 2:
            return 0.0
        step = max(1, n // sample_size)
        sampled_indices = range(0, n - 1, step)
        inversions = sum(1 for i in sampled_indices if self.data[i] > self.data[i + 1])
        total = len(list(sampled_indices))
        return inversions / total if total else 0.0

    def _insertion_sort(self):
        data = self.data
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and data[j] > key:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key

    def _merge_sort(self):
        self.data = self.__merge_sort_recursive(self.data)

    def __merge_sort_recursive(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.__merge_sort_recursive(arr[:mid])
        right = self.__merge_sort_recursive(arr[mid:])
        return self.__merge(left, right)

    def __merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def choose_algorithm(self):
        """Decide which strategy to use based on size and sortedness."""
        n = len(self.data)
        if n <= 1 or self.is_sorted():
            return 'skip'
        if n <= self.SMALL_DATASET_THRESHOLD:
            return 'insertion'
        inversion_ratio = self._count_inversions_sample()
        if inversion_ratio <= self.NEARLY_SORTED_INVERSION_RATIO:
            return 'insertion'
        return 'merge'

    def sort_data(self, verbose=True):
        algo = self.choose_algorithm()
        self.last_algorithm_used = algo

        if algo == 'skip':
            if verbose:
                print("Data is already sorted (or trivial size). Skipping sort.")
            return 0.0

        if verbose:
            print(f"Sorting using: {algo.upper()} SORT")

        start = time.time()
        if algo == 'insertion':
            self._insertion_sort()
        elif algo == 'merge':
            self._merge_sort()
        elapsed = time.time() - start

        if verbose:
            print(f"Sort Time: {elapsed:.6f} seconds")
        return elapsed

    def search(self, target, verbose=True):
        """Binary search — assumes data is sorted (call sort_data() first)."""
        start = time.time()
        left, right = 0, len(self.data) - 1
        found = False

        while left <= right:
            mid = (left + right) // 2
            if self.data[mid] == target:
                found = True
                break
            elif self.data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        elapsed = time.time() - start
        if verbose:
            print(f"Search Time: {elapsed:.6f} seconds")
        return found


if __name__ == "__main__":
    system = AdaptiveSortingSearchingSystem('composite')

    names = ["Ibrahim", "Muzammil", "Hamza", "Sudais", "Aoun", "Zain", "Ashkan", "Amaan"]
    num_records = 10000

    print(f"Inserting {num_records} records...")
    start = time.time()
    for i in range(num_records):
        random_id = random.randint(1, 10000)
        random_name = random.choice(names)
        system.insert(CompositeKey(random_id, random_name))
    end = time.time()
    print(f"Insertion Time: {end - start:.6f} seconds")

    system.sort_data()
    print(f"Algorithm chosen: {system.last_algorithm_used}")

    print("\nSorted Data Sample (Index 100 to 110):")
    for i in range(100, 111):
        print(system.data[i])

    print("\nSearching for (5000, 'Zain'):")
    target = CompositeKey(5000, "Zain")
    found = system.search(target)
    print("Found:", found)