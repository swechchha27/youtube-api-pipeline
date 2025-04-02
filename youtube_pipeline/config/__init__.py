from configparser import ConfigParser
from pathlib import Path

PROJECTROOT = Path(__file__).parent.parent.parent
CONFIGFILEPATH = Path(__file__).parent / 'pipeline_config.ini'

pipeline_config = ConfigParser()
pipeline_config.read(CONFIGFILEPATH)

DATACONFIG = pipeline_config['DATA']
DATAFOLDER = PROJECTROOT / DATACONFIG['DATA_FOLDER']
TESTFOLDER = PROJECTROOT / pipeline_config['TEST']['TEST_FOLDER']
LOGFOLDER = PROJECTROOT /  pipeline_config['LOG']['LOG_FOLDER']
APICONFIG = pipeline_config['YOUTUBE_API']
DBCONFIG = pipeline_config['DATABASE']
DBSCRIPTFOLDER = PROJECTROOT / DBCONFIG['DBSCRIPT_FOLDER']

print('*'*50)
print('Configuration imported')
print('*'*50)