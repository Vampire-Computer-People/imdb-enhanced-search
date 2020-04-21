import pandas as pd
import requests
import os

UNICODE_ESCAPE = 'unicode_escape'


class Build:
    def __init__(self, encoding, merge_column, imdb_url, input_separator, null_char):
        self.input_separator = input_separator
        self.null_char = null_char
        self.encoding = encoding
        self.merge_column = merge_column
        self.imdb_url = imdb_url

    def sanitize(self, data):
        nchar = self.null_char.encode().decode(UNICODE_ESCAPE)
        for key in data:
            try:
                print('Sanitizing data on {}'.format(key))
                data[key].replace({nchar: None}, inplace=True)
            except TypeError:
                print('Got a TypeError - should not be an issue...')

    def read_data(self, name):
        print('Reading {}...'.format(name))
        isep = self.input_separator.encode().decode(UNICODE_ESCAPE)
        result = pd.read_csv(name, sep=isep, encoding=self.encoding)
        print('Deleting {}...'.format(name))
        os.remove(name)
        return result

    def download_imdb_data(self, name):
        full_path = '{}/{}'.format(self.imdb_url, name)
        print('Downloading data from {}...'.format(full_path))
        r = requests.get(full_path)
        print('Writing file...')
        open(name, 'wb').write(r.content)

    def merge(self, data_left, data_right):
        print('Merging data...')
        return pd.merge(data_left, data_right, on=self.merge_column)

    def write_file(self, data, file_name):
        print('Writing file...')
        data.to_csv(file_name, encoding=self.encoding)
