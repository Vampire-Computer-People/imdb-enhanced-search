import csv
import random
import webbrowser
import configparser


class Filter:
    def __init__(self, config_file, data_filename, encoding, imdb_id, browser_url):
        self.imdb_id = imdb_id
        self.browser_url = browser_url
        self.filters = None
        self.imdb_columns = None
        self.imdb_filter_strings = None

        self._parse_config(config_file)
        self.data = self._load_data(data_filename, encoding)

    def _parse_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self.filters = config['FILTERS']
        self.imdb_columns = config['IMDB_COLUMNS']
        self.imdb_filter_strings = config['IMDB_FILTER_STRINGS']

    def _load_data(self, data_filename, encoding):
        print('Building films into memory...')
        return csv.DictReader(open(data_filename, encoding=encoding))

    def run_filters(self):
        print('Filtering films...')
        filtered = []

        # Rating ---
        avg_column = self.imdb_columns['AverageRating']

        min_rating = self.filters['MinimumRating']

        print('Rated at least {}'.format(min_rating))
        # Check that average column exists before checking value
        filtered[:] = [mv for mv in self.data if (avg_column in mv and float(mv[avg_column]) >= float(min_rating))]
        self.data = filtered

        # Popularity ---
        num_votes_column = self.imdb_columns['NumberVotes']
        min_votes = self.filters['MinimumNumberVotes']
        max_votes = self.filters['MaximumNumberVotes']

        print('With at least {} reviews but no more than {}'.format(str(min_votes), max_votes))
        filtered[:] = [mv for mv in self.data if
                       (int(mv[num_votes_column]) >= int(min_votes) and int(mv[num_votes_column]) <= int(max_votes))]
        self.data = filtered

        # Modernity ---
        start_yr_column = self.imdb_columns['StartYear']
        min_yr = self.filters['MinimumYear']

        print('Made after or on {}'.format(min_yr))
        filtered[:] = [mv for mv in self.data if not mv[start_yr_column] or int(mv[start_yr_column]) >= int(min_yr)]
        self.data = filtered

        # Genre Filter ---
        if self.filters['GenreFilter'].lower().strip() == 'yes':
            genre_column = self.imdb_columns['Genres']
            genres = self.imdb_filter_strings['Genres']

            for genre in genres.split(','):
                g = genre.strip()
                print('With a genre of {}'.format(g))
                filtered[:] = [mv for mv in self.data if g in mv[genre_column]]
                self.data = filtered

        # TV exclusion ---
        tv_results = self.filters['TVResults'].lower().strip()
        title_type_column = self.imdb_columns['TitleType']

        if tv_results == 'no':
            tv_string = self.imdb_filter_strings['TvString']

            print('No TV')
            filtered[:] = [mv for mv in self.data if tv_string not in mv[title_type_column]]
            self.data = filtered

        # Video Games exclusion ---
        vg_results = self.filters['VideoGamesResults'].lower().strip()

        if vg_results == 'no':
            vg_string = self.imdb_filter_strings['VideoGameString']

            print('No video games')
            filtered[:] = [mv for mv in self.data if vg_string not in mv[title_type_column]]
            self.data = filtered

        print('Got {} result(s)'.format(len(self.data)))

    def pick(self):
        title = self.imdb_columns['PrimaryTitle']

        print('Picking random film...')
        try:
            random_movie = random.choice(self.data)
            self.data.remove(random_movie)
            imdb_id = random_movie[self.imdb_id]
            title = random_movie[title]
            url = '{}/{}'.format(self.browser_url, imdb_id)
            print('Opening "{}" at {} ...'.format(title, url))
            print('{} result(s) left'.format(len(self.data)))
            webbrowser.open(url)
        except IndexError:
            print('No films found/left!')
