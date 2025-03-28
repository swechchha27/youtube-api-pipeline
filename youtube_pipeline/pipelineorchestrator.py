from dataextractor import YoutubeDataExtractor
from pathlib import Path
from config import pipeline_config as pipeconfig
from datetime import datetime
import pandas as pd

def main():
    ETL = YoutubeDataExtractor()
    # if data/categories.csv is a month older or older, then fetch the categories again
    root_folder = Path(__file__).parent.parent
    categories_file = root_folder / pipeconfig['DATA']['DATA_FOLDER'] / pipeconfig['DATA']['CATEGORIES_FILE']
    prev_month_timestamp = datetime.now().timestamp() - 30 * 24 * 60 * 60
    if not categories_file.exists() or (categories_file.stat().st_mtime < prev_month_timestamp):
        print("\nFetching categories again as its been a month...")
        ETL.list_categories()
    else:
        print(f"\nCategories file {categories_file} is up to date.")
    categories_df = pd.read_csv(categories_file)
    # Fetch list of category_id of categories that have title like 'game' or 'gaming'
    category_list = categories_df[categories_df['title'].str.contains('game|gaming|sport', case=False)]['category_id'].values.tolist()
    print(category_list)
    # for category in category_list:
    #     print(f"Fetching videos for category {category}...")
    #     videos = ETL.search_by_keyword(
    #         query='game|games +android',
    #         categoryId=category,
    #         maxResults=5
    #         )
    #     print(videos)
    for category in category_list:
        videos = ETL.get_popular_videos(
            categoryId=category,
            maxResults=5
        )
        print(videos)

if __name__ == '__main__':
    main()
    