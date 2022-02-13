import WatchStatusDBM as db
from sqlite3 import Error


# TODO: Check if episode being downloaded. If it is-> update. If it doesn't-> Alert user.
# TODO: Re-watching mode - In case the user wants to re-download a series.
# TODO: Downloader won't save series to database if it didn't find anything

class Series:
    def __init__(self, name: str, is_all=False):
        name = name.lower()
        self.all = is_all
        self.season = None
        try:
            self.database_connector = db.init_database()
        except Error as err:
            self.exception_initiation(err, name)
            return
        with self.database_connector as conn:
            series_data = db.select_series_by_name(conn, name)
            if len(series_data) == 0:
                self._init_new_series(name)
            else:
                (self.name, self.season, self.episode) = series_data[0]

    def _init_new_series(self, name: str):
        self.name = name
        self.season = int(input('Enter season: '))
        self.episode = 1
        db.create_series(self.database_connector, (self.name, self.season, self.episode))

    def get_episode_str(self):
        return '0' + str(self.episode) if self.episode < 10 else str(self.episode)

    def get_season_str(self):
        return '0' + str(self.season) if self.season < 10 else str(self.season)

    def update_episode(self):
        try:
            with self.database_connector as conn:
                db.update_series(conn, (self.season, self.episode, self.name))
        except Error as err:
            print(err)
            series_list = db.select_series_by_name(conn, self.name)
            if self.season != series_list[1] or self.episode != series_list[2]:
                print("DATA DID NOT UPDATED.")
                exit(1)

    def exception_initiation(self, db_error: Error, name: str):
        print(db_error)
        print('Doing Action without connection to database!')
        self._init_new_series(name)

    def __str__(self):
        return self.name + ' s' + self.get_season_str() + 'e' + self.get_episode_str()

    def create_episode_path(self, episode_torrent_name: str, torrent_path=""):
        db.create_episode(self.database_connector,
                          (self.name, self.season, self.episode, episode_torrent_name, torrent_path))

    @staticmethod
    def delete_series_by_name(series_to_be_deleted: str):
        try:
            database_connector = db.init_database()
            with database_connector as conn:
                db.delete_episodes(conn, series_to_be_deleted)
                db.delete_series(conn, series_to_be_deleted)
        except Error as err:
            print("Deletion failed.")
