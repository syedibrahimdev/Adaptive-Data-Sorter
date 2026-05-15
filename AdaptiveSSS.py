import random
from dataclasses import dataclass
import time

@dataclass(order=True)
class CompositeKey:
    id: int
    name: str

    def __str__(self):
        return f"({self.id}, {self.name})"

class AdaptiveSortingSearchingSystem:
    def __init__(self, key_type):
        self.key_type = key_type  # 'int', 'str', or 'composite'
        self.data = []

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

    def sort_data(self):
        if self.is_sorted():
            print("Data is already sorted. Skipping sort.")
            return

        print("Sorting data...")
        start = time.time()
        self.data.sort()
        end = time.time()
        print(f"Sort Time: {end - start:.6f} seconds")

    def search(self, target):
        start = time.time()
        left = 0
        right = len(self.data) - 1

        while left <= right:
            mid = (left + right) // 2
            if self.data[mid] == target:
                end = time.time()
                print(f"Search Time: {end - start:.6f} seconds")
                return True
            elif self.data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        end = time.time()
        print(f"Search Time: {end - start:.6f} seconds")
        return False

if __name__ == "__main__":
    system = AdaptiveSortingSearchingSystem('composite')
    # system.insert(CompositeKey(2, "Ibrahim"))
    # system.insert(CompositeKey(1, "Arham"))
    # system.insert(CompositeKey(3, "Yousef"))
    # system.insert(CompositeKey(5, "Sabeer"))
    # system.insert(CompositeKey(4, "Muzammil"))

    # print("Current Data:")
    # print("Before sorting:")
    # system.print_data()

    # system.sort_data()

    # print("\nAfter sorting:")
    # system.print_data()

    # print("\nDeleting (1, Arham):")
    # system.delete(CompositeKey(1, "Arham"))
    # system.print_data()

    # print("\nSearching for (3, Yousef)")
    # print(system.search(CompositeKey(3, "Yousef")))

    # print("Searching for (6, Hamza):")
    # print(system.search(CompositeKey(6, "Hamza")))

    # ---TESTING WITH LARGE DATA SETS---

    # system.insert(CompositeKey(5000, "Zain"))  # Ensures it exists

    # Define test parameters
    names = ["Ibrahim", "Muzammil", "Hamza", "Sudais", "Aoun", "Zain", "Ashkan", "Amaan"]
    num_records = 10000

    # Generate random data
    print(f"Inserting {num_records} records...")
    start = time.time()
    for i in range(num_records):
        random_id = random.randint(1, 10000)
        random_name = random.choice(names)
        system.insert(CompositeKey(random_id, random_name))
    end = time.time()
    print(f"Insertion Time: {end - start:.6f} seconds")


    # Sort the data
    system.sort_data()
    print("\nSorted Data Sample (Index 100 to 110):")
    for i in range(100, 111):
        print(system.data[i])

    # Search for a specific record
    print("\nSearching for (5000, 'Zain'):")
    target = CompositeKey(5000, "Zain")
    found = system.search(target)
    print("Found:", found)
