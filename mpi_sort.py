from mpi4py import MPI
import numpy as np
import time

MAX_INT = 1000000
TOTAL_SIZE = 1000000

def parallel_sort():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Initialize timing dictionary
    timing = {}
    
    # Generate data only on root process
    if rank == 0:
        start_time = time.time()
        # Example: Create random data
        data = np.random.randint(0, MAX_INT, TOTAL_SIZE)
        timing['data_generation'] = time.time() - start_time
        
        # Calculate and print initial data statistics
        print(f"\nInitial Data Statistics:")
        
        # Calculate chunk size
        chunk_size = len(data) // size
    else:
        data = None
        chunk_size = None
    
    # Broadcast chunk size to all processes
    start_time = time.time()
    chunk_size = comm.bcast(chunk_size, root=0)
    timing['broadcast'] = time.time() - start_time
    
    # Scatter data across processes
    start_time = time.time()
    local_chunk = np.empty(chunk_size, dtype=np.int64)
    comm.Scatter(data, local_chunk, root=0)
    timing['scatter'] = time.time() - start_time
    
    # Sort local data
    start_time = time.time()
    local_chunk.sort()
    timing['local_sort'] = time.time() - start_time
    
    # Print local process statistics
    print(f"\nSorting in process {rank}")
    
    # Gather all sorted chunks back to root
    start_time = time.time()
    if rank == 0:
        sorted_data = np.empty_like(data)
    else:
        sorted_data = None
    comm.Gather(local_chunk, sorted_data, root=0)
    timing['gather'] = time.time() - start_time
    
    # Perform final merge on root
    if rank == 0:
        start_time = time.time()
        sorted_data.sort()
        timing['final_merge'] = time.time() - start_time
        
        # Print final statistics
        print(f"\nFinal Sorted Data Statistics:")
        print(f"Total size: {len(sorted_data)}")
        print(f"Range: [{np.min(sorted_data)}, {np.max(sorted_data)}]")
        print(f"Mean: {np.mean(sorted_data):.2f}")
        
        # Print timing information
        print("\nTiming Information:")
        total_time = sum(timing.values())
        for stage, time_taken in timing.items():
            print(f"{stage}: {time_taken:.4f} seconds ({(time_taken/total_time)*100:.1f}%)")
        print(f"Total time: {total_time:.4f} seconds")
        
        return sorted_data
    return None

if __name__ == "__main__":
    result = parallel_sort()
    if MPI.COMM_WORLD.Get_rank() == 0:
        print("\nFirst 10 elements of sorted array:", result[:10])