import pandas as pd

def main():
    # Read the movie ratings summary
    ratings_summary = pd.read_csv('output/movie_ratings_summary.csv')

    # Read the movie metadata
    movie_metadata = pd.read_csv('input-netflix/Netflix_Dataset_Movie.csv')

    # Merge the datasets on Movie_ID
    merged_data = pd.merge(ratings_summary, movie_metadata, on='Movie_ID')

    # Group by Year
    grouped_data = merged_data.groupby('Year')

    # Initialize lists to store results
    top_movies = []
    worst_movies = []

    # Iterate over each year
    for year, group in grouped_data:
        # Find the top movie (highest average rating)
        top_movie = group.loc[group['Average_Rating'].idxmax()]
        top_movies.append({
            'Year': year,
            'Name': top_movie['Name'],
            'Average_Rating': top_movie['Average_Rating'],
            'Total_Ratings': top_movie['Total_Ratings']
        })

        # Find the worst movie (lowest average rating)
        worst_movie = group.loc[group['Average_Rating'].idxmin()]
        worst_movies.append({
            'Year': year,
            'Name': worst_movie['Name'],
            'Average_Rating': worst_movie['Average_Rating'],
            'Total_Ratings': worst_movie['Total_Ratings']
        })

    # Convert results to DataFrames
    top_movies_df = pd.DataFrame(top_movies)
    worst_movies_df = pd.DataFrame(worst_movies)

    # Save the results to CSV files
    top_movies_df.to_csv('output/top_movies_by_year.csv', index=False)
    worst_movies_df.to_csv('output/worst_movies_by_year.csv', index=False)
    
    # Print all results
    print("\nTop Movies by Year:")
    print(top_movies_df)
    print("\nWorst Movies by Year:")
    print(worst_movies_df)

if __name__ == "__main__":
    main()