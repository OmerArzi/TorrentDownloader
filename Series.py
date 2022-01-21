import WatchStatusDBM as db
from sqlite3 import Error


class Series:
    def __init__(self, name: str, season: int, is_all=False):
        try:
            database_connector = db.init_database()
        except Error as err:
            self.exception_initiation(err,name, season)
            return
        with database_connector as conn:
            series_data = db.select_series_by_name(conn, name)
            self.all = is_all
            if len(series_data) == 0:
                self._init_new_series(conn, name, season)
            else:
                [self.name, self.season, self.episode] = series_data

    def _init_new_series(self, database_connector, name: str, season: int):
        self.name = name
        self.season = season
        self.episode = 1
        db.create_series(database_connector, (self.name, self.season, self.episode))

    def get_episode_str(self):
        return '0' + str(self.episode) if self.episode < 10 else str(self.episode)

    def get_season_str(self):
        return '0' + str(self.season) if self.season < 10 else str(self.season)

    def update_episode(self):
        try:
            database_connector = db.init_database()
            with database_connector as conn:
                conn.update_series(conn, (self.season, self.episode, self.name))
        except Error as err:
            print(err)
            series_list = db.select_series_by_name(self.name)
            if self.season != series_list[1] or self.episode != series_list[2]:
                print("DATA DID NOT UPDATED.")

    def exception_initiation(self, db_error: Error, name: str, season: int):
        print(db_error)
        print('Doing Action without connection to database!')
        self._init_new_series(name, season)

    def __str__(self):
        return self.name + ' s' + self.get_season_str() + 'e' + self.get_episode_str()
