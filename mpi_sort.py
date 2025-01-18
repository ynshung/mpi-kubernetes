# mpi_sort.py
from mpi4py import MPI
import numpy as np

def parallel_sort():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Generate data only on root process
    if rank == 0:
        # Example: Create random data
        data = np.random.randint(0, 1000, 1000)
        # Calculate chunk size
        chunk_size = len(data) // size
    else:
        data = None
        chunk_size = None
    
    # Broadcast chunk size to all processes
    chunk_size = comm.bcast(chunk_size, root=0)
    
    # Scatter data across processes
    local_chunk = np.empty(chunk_size, dtype=np.int64)
    comm.Scatter(data, local_chunk, root=0)
    
    # Sort local data
    local_chunk.sort()
    
    # Gather all sorted chunks back to root
    if rank == 0:
        sorted_data = np.empty_like(data)
    else:
        sorted_data = None
        
    comm.Gather(local_chunk, sorted_data, root=0)
    
    # Perform final merge on root
    if rank == 0:
        sorted_data.sort()
        return sorted_data
    
    return None

if __name__ == "__main__":
    result = parallel_sort()
    if MPI.COMM_WORLD.Get_rank() == 0:
        print("Sorted array:", result)