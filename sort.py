import numpy as np
import time

MAX_INT = 1000000000000000
TOTAL_SIZE = 100000000

def parallel_sort():
    timing = {}
    
    # Generate data
    start_time = time.time()
    data = np.random.randint(0, MAX_INT, TOTAL_SIZE)
    timing['data_generation'] = time.time() - start_time
    
    # Sort data
    start_time = time.time()
    data.sort()
    timing['sort'] = time.time() - start_time
    
    # Print timing information
    print("\nTiming Information:")
    total_time = sum(timing.values())
    for stage, time_taken in timing.items():
        print(f"{stage}: {time_taken:.4f} seconds ({(time_taken/total_time)*100:.1f}%)")
    print(f"Total time: {total_time:.4f} seconds")
    
    return data

if __name__ == "__main__":
    result = parallel_sort()
    print("\nFirst 10 elements of sorted array:", result[:10])
