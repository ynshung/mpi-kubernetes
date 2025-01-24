from mpi4py import MPI
import pandas as pd
import numpy as np
import time

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Dictionary to store timing results
    total_time = {
        'file_distribution': 0.0,
        'scatter': 0.0,
        'movie_stats_calculation': 0.0,
        'gather': 0.0,
        'merge_export': 0.0
    }

    if rank == 0:
        # Start timing file distribution
        start_time = time.time()

        # Read the CSV file
        df = pd.read_csv('/app/input-netflix/Netflix_Dataset_Rating.csv')
        
        # Split the data into chunks for each process
        data = np.array_split(df, size)

        # End timing file distribution
        total_time['file_distribution'] = time.time() - start_time

    else:
        data = None

    # Start timing scatter
    scatter_start_time = time.time()

    # Scatter the data to all processes
    data = comm.scatter(data, root=0)

    # End timing scatter
    total_time['scatter'] = time.time() - scatter_start_time

    # Start timing movie stats calculation
    movie_stats_start_time = time.time()

    # Calculate total ratings and average rating for each movie in the chunk
    movie_stats = data.groupby('Movie_ID').agg(
        Total_Ratings=('Rating', 'count'),
        Average_Rating=('Rating', 'mean')
    ).reset_index()

    # End timing movie stats calculation
    total_time['movie_stats_calculation'] = time.time() - movie_stats_start_time

    # Start timing gather
    gather_start_time = time.time()

    # Gather all results at the root process
    gathered_stats = comm.gather(movie_stats, root=0)

    # End timing gather
    total_time['gather'] = time.time() - gather_start_time

    if rank == 0:
        # Start timing merge and export
        merge_export_start_time = time.time()

        # Concatenate all gathered results
        final_stats = pd.concat(gathered_stats)
        
        # Group by Movie_ID again to combine results from different chunks
        final_stats = final_stats.groupby('Movie_ID').agg(
            Total_Ratings=('Total_Ratings', 'sum'),
            Average_Rating=('Average_Rating', 'mean')
        ).reset_index()

        # Sort by Average_Rating in descending order
        final_stats = final_stats.sort_values(by='Average_Rating', ascending=False)

        # Save to a new CSV file
        final_stats.to_csv('output/movie_ratings_summary.csv', index=False)

        # End timing merge and export
        total_time['merge_export'] = time.time() - merge_export_start_time

        # Print timing results
        print("Timing Results:")
        print(f"File Distribution Time: {total_time['file_distribution']:.4f} seconds")
        print(f"Scatter Time: {total_time['scatter']:.4f} seconds")
        print(f"Movie Stats Calculation Time: {total_time['movie_stats_calculation']:.4f} seconds")
        print(f"Gather Time: {total_time['gather']:.4f} seconds")
        print(f"Merge and Export Time: {total_time['merge_export']:.4f} seconds")
        print(f"Total Execution Time: {sum(total_time.values()):.4f} seconds")

if __name__ == "__main__":
    main()