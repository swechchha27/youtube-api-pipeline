from pathlib import Path
from config import *
from googleapiclient.discovery import build
from datatransformer import *


yc = pipeline_config['YOUTUBE_API']

class YoutubeDataExtractor:
    def __init__(self):
        self.youtube_object = build(serviceName=yc['SERVICE'], version=yc['VERSION'], developerKey=yc['KEY'])
    
    '''
    This method fetches the most popular videos from YouTube based on the provided keyword,
    optionally the specified region and maximum results.
    It returns a list of dictionaries containing video details,
    and converts it into a pandas DataFrame.
    '''
    def search_by_keyword(self, query, categoryId = None, order='relevance', publishedAfter=None , region=None, maxResults=5):
        response = self.youtube_object.search().list(
            q=query,
            part='id,snippet',
            type='video',
            publishedAfter=publishedAfter,
            order=order,
            regionCode=region,
            videoCategoryId=categoryId,
            maxResults=maxResults
        ).execute()
        search_results = response.get('items', [])
        videos = []
        for search_result in search_results:
            if search_result['id']['kind'] == 'youtube#video':
                # Append the list with video details converted into dictionary format
                videos.append(
                    {
                        'video_id': search_result['id']['videoId'],
                        'video_title': search_result['snippet']['title'],
                        'description': search_result['snippet']['description'],
                        'published_at': search_result['snippet']['publishedAt'],
                        'channel_id': search_result['snippet']['channelId'],
                        'channel_title': search_result['snippet']['channelTitle'],
                    }
                )
            else:
                raise Exception(f'Invalid result type: {search_result["id"]["kind"]}')
        df = convert_to_dataframe(videos)
        return df
    
    '''This method fetches all the video categories available on YouTube.
    It returns a list of dictionaries containing category details,
    and converts it into a pandas DataFrame, then spools it to a CSV file
    'categories.csv'
    in data folder under root of project.
    '''
    def list_categories(self, region='US'):
        response = self.youtube_object.videoCategories().list(
            part='snippet',
            regionCode=region
        ).execute()
        # print(response)
        categories = []
        for item in response['items']:
            categories.append(
                {
                    'category_id': item['id'],
                    'category_title': item['snippet']['title']
                }
            )
        df = convert_to_dataframe(categories)
        df.to_csv(Path(__file__).parent.parent / 'data' / 'categories.csv', index=False)
        return df
    
    '''THis method fetches the most popular videos from videos.list endpoint based on category'''
    def get_popular_videos(self, categoryId=None, maxResults=5):
        response = self.youtube_object.videos().list(
            part='snippet,contentDetails,statistics',
            chart='mostPopular',
            videoCategoryId=categoryId,
            maxResults=maxResults
        ).execute()
        videos = []
        for item in response['items']:
            videos.append(
                {
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
                }
            )
        df = convert_to_dataframe(videos)
        return df
    
    '''THis method fetches the details of provided videos from videos.list endpoint'''
    def get_video_details(self, videoIdList, maxResults=5):
        response = self.youtube_object.videos().list(
            part='snippet,contentDetails,statistics,topicDetails',
            id=','.join(videoIdList),
            maxResults=maxResults
        ).execute()
        videos = []
        for item in response['items']:
            videos.append(
                {
                    'video_id': item['id'],
                    'video_title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'localized_title': item['snippet']['localized']['title'],
                    'localized_description': item['snippet']['localized']['description'],
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
                    'comment_count': item['statistics'].get('commentCount', 0),
                    'favorite_count': item['statistics'].get('favoriteCount', 0),
                    'topic_categories': item['topicDetails'].get('topicCategories', []),
                }
            )
        # print(videos)
        df = convert_to_dataframe(videos)
        return df