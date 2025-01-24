import pandas as pd
import numpy as np
import time

def main():
    start_time = time.time()
    
    # Read the CSV file
    df = pd.read_csv('/app/input-netflix/Netflix_Dataset_Rating.csv')

    # Calculate total ratings and average rating for each movie
    movie_stats = df.groupby('Movie_ID').agg(
        Total_Ratings=('Rating', 'count'),
        Average_Rating=('Rating', 'mean')
    ).reset_index()

    # Sort by Average_Rating in descending order
    movie_stats = movie_stats.sort_values(by='Average_Rating', ascending=False)

    # Save to a new CSV file
    movie_stats.to_csv('output/movie_ratings_summary.csv', index=False)
    print("Results saved to 'output/movie_ratings_summary.csv'")
    
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()