from mpi4py import MPI
import os
import csv
from collections import defaultdict
import time

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Directory containing the files
input_dir = "input-now"

# Function to count words in a file
def count_words_in_file(file_path):
    word_count = defaultdict(int)
    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split()
            for word in words:
                word_count[word.lower()] += 1
    return word_count

# Function to merge word counts from multiple dictionaries
def merge_word_counts(word_counts):
    merged = defaultdict(int)
    for wc in word_counts:
        for word, count in wc.items():
            merged[word] += count
    return merged

# Root process: Distribute files among processes
if rank == 0:
    start_time = time.time()  # Start timing for file distribution
    # Get list of files in the directory
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    # Split files into chunks for each process
    chunks = [[] for _ in range(size)]
    for i, file in enumerate(files):
        chunks[i % size].append(file)
    file_distribution_time = time.time() - start_time  # End timing for file distribution
else:
    chunks = None
    file_distribution_time = 0

# Scatter file chunks to all processes
start_time = time.time()  # Start timing for scattering
chunk = comm.scatter(chunks, root=0)
scatter_time = time.time() - start_time  # End timing for scattering

# Each process counts words in its assigned files
start_time = time.time()  # Start timing for word counting
local_word_count = defaultdict(int)
for file in chunk:
    wc = count_words_in_file(file)
    for word, count in wc.items():
        local_word_count[word] += count
word_counting_time = time.time() - start_time  # End timing for word counting

# Gather all local word counts to the root process
start_time = time.time()  # Start timing for gathering
all_word_counts = comm.gather(local_word_count, root=0)
gather_time = time.time() - start_time  # End timing for gathering

# Root process merges the results and writes to CSV
if rank == 0:
    start_time = time.time()  # Start timing for merging and exporting
    # Merge word counts from all processes
    final_word_count = merge_word_counts(all_word_counts)
    
    # Sort words alphabetically
    sorted_words = sorted(final_word_count.items(), key=lambda x: x[0])
    
    # Write to CSV
    with open('output/word_counts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Word', 'Count'])
        for word, count in sorted_words:
            writer.writerow([word, count])
    merge_export_time = time.time() - start_time  # End timing for merging and exporting
else:
    merge_export_time = 0

# Gather timing results from all processes
timing_data = comm.gather({
    'file_distribution': file_distribution_time,
    'scatter': scatter_time,
    'word_counting': word_counting_time,
    'gather': gather_time,
    'merge_export': merge_export_time
}, root=0)

# Root process prints the timing results
if rank == 0:
    total_time = {
        'file_distribution': 0,
        'scatter': 0,
        'word_counting': 0,
        'gather': 0,
        'merge_export': 0
    }
    for data in timing_data:
        for key in total_time:
            total_time[key] += data[key]
    
    print("Timing Results:")
    print(f"File Distribution Time: {total_time['file_distribution']:.4f} seconds")
    print(f"Scatter Time: {total_time['scatter']:.4f} seconds")
    print(f"Word Counting Time: {total_time['word_counting']:.4f} seconds")
    print(f"Gather Time: {total_time['gather']:.4f} seconds")
    print(f"Merge and Export Time: {total_time['merge_export']:.4f} seconds")
    print(f"Total Execution Time: {sum(total_time.values()):.4f} seconds")