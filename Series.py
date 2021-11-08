class Series:
    def __init__(self, name, season, is_all=False):
        self.name = name
        self.season = season
        self.episode = 1
        self.all = is_all


    def get_episode_str(self):
        if self.episode<10:
            return '0' + str(self.episode)
        else:
            return str(self.episode)

    def get_season_str(self):
        if self.season<10:
            return '0' + str(self.season)
        else:
            return str(self.season)

    def __str__(self):
        return self.name + ' s' + self.get_season_str() + 'e' + self.get_episode_str()

