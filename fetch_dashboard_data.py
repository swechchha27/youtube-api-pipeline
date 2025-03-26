import matplotlib.pyplot as plt
import seaborn as sns
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
    # check for missing values
    missing_values = trending_videos.isnull().sum()
    # display data types
    data_types = trending_videos.dtypes
    # fill missing descriptions with "No description"
    trending_videos['description'].fillna('No description', inplace=True)
    # convert `published_at` to datetime
    trending_videos['published_at'] = pd.to_datetime(trending_videos['published_at'])
    # convert tags from string representation of list to actual list
    trending_videos['tags'] = trending_videos['tags'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    # descriptive statistics
    descriptive_stats = trending_videos[['view_count', 'like_count', 'dislike_count', 'comment_count']].describe()

    sns.set(style="whitegrid")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # view count distribution
    sns.histplot(trending_videos['view_count'], bins=30, kde=True, ax=axes[0], color='blue')
    axes[0].set_title('View Count Distribution')
    axes[0].set_xlabel('View Count')
    axes[0].set_ylabel('Frequency')

    # like count distribution
    sns.histplot(trending_videos['like_count'], bins=30, kde=True, ax=axes[1], color='green')
    axes[1].set_title('Like Count Distribution')
    axes[1].set_xlabel('Like Count')
    axes[1].set_ylabel('Frequency')

    # comment count distribution
    sns.histplot(trending_videos['comment_count'], bins=30, kde=True, ax=axes[2], color='red')
    axes[2].set_title('Comment Count Distribution')
    axes[2].set_xlabel('Comment Count')
    axes[2].set_ylabel('Frequency')

    plt.tight_layout()
    # plt.show()
    
    # correlation matrix
    correlation_matrix = trending_videos[['view_count', 'like_count', 'comment_count']].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, linecolor='black')
    plt.title('Correlation Matrix of Engagement Metrics')
    plt.show()