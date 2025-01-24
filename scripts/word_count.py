import os
import csv
from collections import defaultdict
import time

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

# Main function
def main():
    start_time = time.time()  # Start timing for the entire process

    # Stage 1: File Distribution (List files)
    stage1_start = time.time()
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    stage1_time = time.time() - stage1_start

    # Stage 2: Word Counting
    stage2_start = time.time()
    all_word_counts = []
    for file in files:
        wc = count_words_in_file(file)
        all_word_counts.append(wc)
    stage2_time = time.time() - stage2_start

    # Stage 3: Merge Word Counts
    stage3_start = time.time()
    final_word_count = merge_word_counts(all_word_counts)
    stage3_time = time.time() - stage3_start

    # Stage 4: Export to CSV
    stage4_start = time.time()
    # Sort words alphabetically
    sorted_words = sorted(final_word_count.items(), key=lambda x: x[0])
    # Write to CSV
    with open('output/word_counts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Word', 'Count'])
        for word, count in sorted_words:
            writer.writerow([word, count])
    stage4_time = time.time() - stage4_start

    # Total execution time
    total_time = time.time() - start_time

    # Print timing results
    print("Timing Results:")
    print(f"File Listing Time: {stage1_time:.4f} seconds")
    print(f"Word Counting Time: {stage2_time:.4f} seconds")
    print(f"Merge Word Counts Time: {stage3_time:.4f} seconds")
    print(f"Export to CSV Time: {stage4_time:.4f} seconds")
    print(f"Total Execution Time: {total_time:.4f} seconds")

if __name__ == "__main__":
    main()