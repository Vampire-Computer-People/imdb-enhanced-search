import build
import filter
import configparser
from os import path

CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()
config.read(path.join(path.dirname(__file__), CONFIG_FILE))

SYS_DATA = config['SYSTEM']
DATA_FILE_NAME = SYS_DATA['DataFilename']
ENCODING = SYS_DATA['Encoding']
IMDB_ID = SYS_DATA['IMDBID']

if not path.isfile(DATA_FILE_NAME) or SYS_DATA['Rebuild'] == 'yes':
    build = build.Build(
        ENCODING,
        IMDB_ID,
        SYS_DATA['BaseURL'],
        SYS_DATA['InputSeparator'],
        SYS_DATA['NullChar'],
    )
    basics_filename = SYS_DATA['BasicsFilename']
    ratings_filename = SYS_DATA['RatingsFilename']

    build.download_imdb_data(basics_filename)
    build.download_imdb_data(ratings_filename)

    basics = build.read_data(basics_filename)
    ratings = build.read_data(ratings_filename)

    merged = build.merge(basics, ratings)

    build.sanitize(merged)

    build.write_file(merged, DATA_FILE_NAME)


filter = filter.Filter(
    CONFIG_FILE,
    DATA_FILE_NAME,
    ENCODING,
    IMDB_ID,
    SYS_DATA['BaseBrowserURL']
)

filter.run_filters()

while True:
    text = input('press ENTER for a movie...')
    if text == '':
        filter.pick()
    else:
        pass
