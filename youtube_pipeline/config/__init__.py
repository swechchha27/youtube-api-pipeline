from configparser import ConfigParser
from pathlib import Path

pipeline_config = ConfigParser()
pipeline_config.read(Path(__file__).parent / 'pipeline_config.ini')
# print(cparser['YOUTUBE_API'])
print('*'*50)
print('Configuration imported')
print('*'*50)