import os
import pandas as pd
from googleapiclient.discovery import build

# Fetch API key from environment variable
API_KEY = os.getenv('YOUTUBE_API_KEY')
if not API_KEY:
    raise EnvironmentError("YOUTUBE_API_KEY environment variable not set.")

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SYSDATE = pd.Timestamp.now().strftime('%Y-%m-%dT%H:%M:%SZ')
PREVIOUS_YEAR = (pd.Timestamp.now() - pd.DateOffset(years=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

# Build the youtube service
youtube_object = build(serviceName=YOUTUBE_API_SERVICE_NAME, version=YOUTUBE_API_VERSION, developerKey=API_KEY)

def search_by_keyword(query, topicId=None, order='relevance', max_results=5):
    search_response = youtube_object.search().list(
        q=query,
        part='id,snippet',
        type='video',
        publishedAfter=PREVIOUS_YEAR,
        topicId=topicId,
        order=order,
        maxResults=max_results
        ).execute()
    search_results = search_response.get('items', [])
    videos = []
    playlists = []
    channels = []
    for search_result in search_results:
        if search_result['id']['kind'] == 'youtube#video':
            videos.append(
                {
                    'video_title': search_result['snippet']['title'],
                    'video_id': search_result['id']['videoId'],
                    'description': search_result['snippet']['description'],
                    'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
                    'channel_title': search_result['snippet']['channelTitle']
                }
            )
        else:
            raise Exception(f'Invalid result type: {search_result["id"]["kind"]}')
    return videos

def get_trending_videos_by_region(api_key, region='US', max_results=20):
    # Initialize an empty list to store the results
    videos = []
    # Make a request to the API to fetch the most popular videos
    request = youtube_object.videos().list(
        part='snippet,contentDetails,statistics',
        chart='mostPopular',
        regionCode=region,
        maxResults=max_results
    )
    # Paginate through the results if there are more than 50
    while request and len(videos) < max_results:
        response = request.execute()
        for item in response['items']:
            video_details = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                'channel_id': item['snippet']['channelId'],
                'channel_title': item['snippet']['channelTitle'],
                'category_id': item['snippet']['categoryId'],
                'tags': item['snippet'].get('tags', []),
                'duration': item['contentDetails']['duration'],
                'definition': item['contentDetails']['definition'],
                'caption': item['contentDetails'].get('caption', 'false'),
                'view_count': item['statistics'].get('viewCount', 0),
                'like_count': item['statistics'].get('likeCount', 0),
                'dislike_count': item['statistics'].get('dislikeCount', 0),
                'favorite_count': item['statistics'].get('favoriteCount', 0),
                'comment_count': item['statistics'].get('commentCount', 0)
            }
            videos.append(video_details)
        # Get the next page token
        request = youtube_object.videos().list_next(request, response)
    return videos[:max_results]

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
def main():
    # region = 'IN'
    # timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    # print(f'Fetching trending videos for {region} at {timestamp}...')
    # resultcount = 50
    # trending_videos = get_trending_videos_by_region(API_KEY, region=region, max_results=resultcount)
    # filename = f'{region}_trending_videos_{timestamp}.csv'
    filename = 'videos_found.csv'
    videos = search_by_keyword('games|game +android', max_results = 10)
    save_to_csv(videos, filename)
    # print(f'Saved top {len(trending_videos)} videos to {filename}')

if __name__ == '__main__':
    main()