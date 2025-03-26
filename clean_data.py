import pandas as pd
import glob

# Pattern to match the CSV files
pattern = '[A-Z][A-Z]_trending_videos_????????_??????.csv'

# Get all files matching the pattern
files = glob.glob(pattern)

# Process each file
for file in files:
    print(f'Processing {file}...')
    trending_videos = pd.read_csv(file)
    print(trending_videos.head())
    # check for missing values
    missing_values = trending_videos.isnull().sum()
    # display data types
    data_types = trending_videos.dtypes
    print('Missing values:\n', missing_values)
    print('Data types:\n', data_types)
    # fill missing descriptions with "No description"
    trending_videos['description'].fillna('No description', inplace=True)
    # convert `published_at` to datetime
    trending_videos['published_at'] = pd.to_datetime(trending_videos['published_at'])
    # convert tags from string representation of list to actual list
    trending_videos['tags'] = trending_videos['tags'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    # descriptive statistics
    descriptive_stats = trending_videos[['view_count', 'like_count', 'dislike_count', 'comment_count']].describe()
    print('Descriptive statistics:\n', descriptive_stats)