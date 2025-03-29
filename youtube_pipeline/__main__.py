from dataextractor import YoutubeDataExtractor
from pathlib import Path
from config import *
from datetime import datetime
import pandas as pd

def main():
    ETL = YoutubeDataExtractor()
    # if data/categories.csv is a month older or older, then fetch the categories again
    categories_file = PROJECTROOT / DATAFOLDER / DATACONFIG['CATEGORIES_FILE']
    current_timestamp = datetime.now().timestamp()
    prev_month_timestamp = current_timestamp - 30 * 24 * 60 * 60
    if not categories_file.exists() or (categories_file.stat().st_mtime < prev_month_timestamp):
        print("\nFetching categories again as its been a month...")
        ETL.list_categories()
    else:
        print(f"\nCategories file {categories_file} is up to date.")
    # Read the categories file into a pandas DataFrame
    categories_df = pd.read_csv(categories_file)
    # Fetch list of category_id of categories that have the required title
    category_list = categories_df[
        categories_df['category_title'].str.contains(APICONFIG['CATEGORYLIKE'], 
                                            case=False)]['category_id'].values.tolist()
    print(category_list)
    # For all category ids found, we search for top videos filtered by the given search query
    videos_df = pd.DataFrame()
    category = 20
    videos_df = ETL.search_by_keyword(
            query=APICONFIG['SEARCHQUERY'],
            categoryId=category,
            maxResults=1
            )
    print(videos_df)
    # for category in category_list:
    #     print(f"Fetching videos for category {category}...")
    #     videos_df = ETL.search_by_keyword(
    #         query=APICONFIG['SEARCHQUERY'],
    #         categoryId=category,
    #         maxResults=1
    #         )
    #     print(videos_df)
    # For all above videos found, we fetch more details like statistics from videos.list endpoint
    videoIdList = videos_df['video_id'].values.tolist()
    print(f"Fetching details for video {videoIdList}...")
    videoDetails_df = ETL.get_video_details(videoIdList=videoIdList)
    # join videodf and videodetailsdf on video_id, keeping single set of common columns
    videos_df = videos_df.merge(videoDetails_df, on='video_id', how='inner', suffixes=('', '_remove'))
    # remove the duplicate columns
    videos_df.drop([i for i in videos_df.columns if 'remove' in i],
                   axis=1, inplace=True)
    # Merge category details into the videos_df
    categories_df['category_id'] = categories_df['category_id'].astype(str)
    videos_df = videos_df.merge(categories_df, on='category_id', how='inner', suffixes=('', '_remove'))
    # remove the duplicate columns
    videos_df.drop([i for i in videos_df.columns if 'remove' in i],
                   axis=1, inplace=True)
    # spool datafram in csv
    videos_df.to_csv(PROJECTROOT / DATAFOLDER / 'output.csv', index=False)


if __name__ == '__main__':
    main()
    