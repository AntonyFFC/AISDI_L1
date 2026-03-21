# Tylko do testowania, nie jest częścią rozwiązania
import random
import time

class ArrayData:
    def __init__(self, data: list[int], min_val: int, max_val: int):
        self.data = data
        self.min_val = min_val
        self.max_val = max_val
        self.count = len(data)

def median(arrays: list[ArrayData]) -> float:
    curr_min = min(arr.min_val for arr in arrays)
    curr_max = max(arr.max_val for arr in arrays)
    total_max = curr_max
    total_count = sum(arr.count for arr in arrays)

    target = (total_count + 1) // 2

    while curr_min <= curr_max:
        mid = (curr_min + curr_max) // 2
        count_left = 0

        for arr in arrays:
            for x in arr.data:
                if x <= mid:
                    count_left += 1
        
        if count_left < target:
            curr_min = mid + 1
        else:
            curr_max = mid - 1

    if (total_count % 2 == 0):
        count_left = 0
        next_min = total_max
        for arr in arrays:
            for x in arr.data:
                if x <= curr_min:
                   count_left += 1
                elif x > curr_min and x < next_min:
                    next_min = x
        if count_left > target:
            return float(curr_min)
        else:
            return (curr_min + next_min) / 2
    
    return float(curr_min)

def run_test_cases():
    print("--- Basic Test ---")
    basic_arrays = [
        ArrayData([1, 3, 5, 2], 1, 5),
        ArrayData([2, 4, 6, 4, 4], 2, 6),
        ArrayData([7, 8, 9, 8, 1], 1, 9)
    ]
    
    all_data = sorted([x for arr in basic_arrays for x in arr.data])
    n = len(all_data)
    expected = all_data[n // 2] if n % 2 == 1 else (all_data[n // 2 - 1] + all_data[n // 2]) / 2
    
    print(f"Basic test match: {median(basic_arrays) == expected}")


    print("\n--- Massive Test ---")
    m = 20
    arrays = []
    total_elements = 0
    
    print("Generating random data...")
    for _ in range(m):
        size = random.randint(10000, 50000) 
        total_elements += size
        data = [random.randint(0, 10000) for _ in range(size)]
        arrays.append(ArrayData(data, min(data), max(data)))
        
    print(f"Generated {m} arrays with {total_elements:,} total elements.")

    start_time = time.time()
    calculated_median = median(arrays)
    custom_time = time.time() - start_time
    
    start_time = time.time()
    all_combined = []
    for arr in arrays:
        all_combined.extend(arr.data)
    all_combined.sort()
    
    n = len(all_combined)
    if n % 2 == 1:
        expected_median = float(all_combined[n // 2])
    else:
        expected_median = (all_combined[n // 2 - 1] + all_combined[n // 2]) / 2.0
    sort_time = time.time() - start_time

    print("\n--- Results ---")
    print(f"My Median Algorithm : {calculated_median}")
    print(f"Expected Median:         {expected_median}")
    print(f"Match:                   {calculated_median == expected_median}")
    print(f"\nMy Median Algorithm Time:   {custom_time:.4f} seconds")
    print(f"Built-in Sort Time:      {sort_time:.4f} seconds")

if __name__ == "__main__":
    run_test_cases()