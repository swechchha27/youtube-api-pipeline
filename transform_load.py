from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import isodate

API_KEY = 'AIzaSyDo8PM-DQiMqI9kHAu-6h6Ln_VkNKBDSo8'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_category_mapping():
    request = youtube.videoCategories().list(
        part='snippet',
        regionCode='US'
    )
    response = request.execute()
    category_mapping = {}
    for item in response['items']:
        category_id = int(item['id'])
        category_name = item['snippet']['title']
        category_mapping[category_id] = category_name
    return category_mapping

# get the category mapping
category_mapping = get_category_mapping()
print(category_mapping)

file = 'US_trending_videos_20250322_170406.csv'
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

trending_videos['category_name'] = trending_videos['category_id'].map(category_mapping)

# Bar chart for category counts
# plt.figure(figsize=(12, 8))
# sns.countplot(y=trending_videos['category_name'], order=trending_videos['category_name'].value_counts().index, palette='viridis')
# plt.title('Number of Trending Videos by Category')
# plt.xlabel('Number of Videos')
# plt.ylabel('Category')
# plt.show()

# average engagement metrics by category
# category_engagement = trending_videos.groupby('category_name')[['view_count', 'like_count', 'comment_count']].mean().sort_values(by='view_count', ascending=False)

# fig, axes = plt.subplots(1, 3, figsize=(18, 10))

# # view count by category
# sns.barplot(y=category_engagement.index, x=category_engagement['view_count'], ax=axes[0], palette='viridis')
# axes[0].set_title('Average View Count by Category')
# axes[0].set_xlabel('Average View Count')
# axes[0].set_ylabel('Category')

# # like count by category
# sns.barplot(y=category_engagement.index, x=category_engagement['like_count'], ax=axes[1], palette='viridis')
# axes[1].set_title('Average Like Count by Category')
# axes[1].set_xlabel('Average Like Count')
# axes[1].set_ylabel('')

# # comment count by category
# sns.barplot(y=category_engagement.index, x=category_engagement['comment_count'], ax=axes[2], palette='viridis')
# axes[2].set_title('Average Comment Count by Category')
# axes[2].set_xlabel('Average Comment Count')
# axes[2].set_ylabel('')

# plt.tight_layout()
# plt.show()

# convert ISO 8601 duration to seconds
trending_videos['duration_seconds'] = trending_videos['duration'].apply(
    lambda x: isodate.parse_duration(x).total_seconds()
    )

trending_videos['duration_range'] = pd.cut(
    trending_videos['duration_seconds'], 
    bins=[0, 300, 600, 1200, 2400, 3600, 7200], 
    labels=['0-5 min', '5-10 min', '10-20 min', '20-40 min', '40-60 min', '60-120 min'])

# # scatter plot for video length vs view count
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='duration_seconds', y='view_count', data=trending_videos, alpha=0.6, color='purple')
# plt.title('Video Length vs View Count')
# plt.xlabel('Video Length (seconds)')
# plt.ylabel('View Count')
# plt.show()

# # bar chart for engagement metrics by duration range
# length_engagement = trending_videos.groupby('duration_range')[['view_count', 'like_count', 'comment_count']].mean()

# fig, axes = plt.subplots(1, 3, figsize=(18, 8))

# # view count by duration range
# sns.barplot(y=length_engagement.index, x=length_engagement['view_count'], ax=axes[0], palette='magma')
# axes[0].set_title('Average View Count by Duration Range')
# axes[0].set_xlabel('Average View Count')
# axes[0].set_ylabel('Duration Range')

# # like count by duration range
# sns.barplot(y=length_engagement.index, x=length_engagement['like_count'], ax=axes[1], palette='magma')
# axes[1].set_title('Average Like Count by Duration Range')
# axes[1].set_xlabel('Average Like Count')
# axes[1].set_ylabel('')

# # comment count by duration range
# sns.barplot(y=length_engagement.index, x=length_engagement['comment_count'], ax=axes[2], palette='magma')
# axes[2].set_title('Average Comment Count by Duration Range')
# axes[2].set_xlabel('Average Comment Count')
# axes[2].set_ylabel('')

# plt.tight_layout()
# plt.show()

# calculate the number of tags for each video
trending_videos['tag_count'] = trending_videos['tags'].apply(len)

# scatter plot for number of tags vs view count
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='tag_count', y='view_count', data=trending_videos, alpha=0.6, color='orange')
# plt.title('Number of Tags vs View Count')
# plt.xlabel('Number of Tags')
# plt.ylabel('View Count')
# plt.show()

# extract hour of publication
trending_videos['publish_hour'] = trending_videos['published_at'].dt.hour

# bar chart for publish hour distribution
plt.figure(figsize=(12, 6))
sns.countplot(x='publish_hour', data=trending_videos, palette='coolwarm')
plt.title('Distribution of Videos by Publish Hour')
plt.xlabel('Publish Hour')
plt.ylabel('Number of Videos')
plt.show()

# scatter plot for publish hour vs view count
plt.figure(figsize=(10, 6))
sns.scatterplot(x='publish_hour', y='view_count', data=trending_videos, alpha=0.6, color='teal')
plt.title('Publish Hour vs View Count')
plt.xlabel('Publish Hour')
plt.ylabel('View Count')
plt.show()