

MIN_YEAR, MAX_YEAR = 1970, 2024


class Player:
    def __init__(self, player_id, player_name):
        self.total_games_recorded = 0

        self.player_id = player_id
        self.full_name = player_name
        self.position: str = None
        self.weight: int = None
        self.age: int = None
        self.team: str = None
        self.headshot: str = None

        self.stats_list = [
                'offensive_snapPct',
                'offensive_snaps',
                'defensive_snapPct',
                'defensive_snaps',
                'st_snapPct',
                'st_snaps',
                'rushAvg',
                'rushYds',
                'carries',
                'rushTD',
                'receptions',
                'recYds',
                'recAvg',
                'targets',
                'qbr',
                'rtg',
                'passAttempts',
                'passAvg',
                'passTD',
                'passYds',
                'int',
                'passCompletions',
                'totalTackles',
                'soloTackles',
                'forcedFumbles',
                'sacks',
                'defInterceptions',
                'passDeflections'
            ]


        self.stats = {}

    def add_stat(self, season: int, stat_name: str, stat) -> None:
        """add a specific stat for a specific game"""
        assert stat_name in self.stats_list and MIN_YEAR <= season <= MAX_YEAR
        if not season in self.stats: self.stats[season] = {}

        if not stat_name in self.stats[season]: self.stats[season][stat_name] = []
        self.stats[season][stat_name].append(stat)

    def get_stat_overall(self, stat_name: str) -> list:
        overall = []
        for season in self.stats.values():
            overall += season[stat_name]
        #assert len(overall) > 0
        return overall

    def print_stats(self):
        print('Player Name: ' + self.full_name)
        for stat_name in self.stats_list:
            print(stat_name + ':' + str(self.get_stat_overall(stat_name)))
            print()








    def offensive_rating(self, weights: list[float]) -> float:
        pass

    def defensive_rating(self, weights: list[float]) -> float:
        pass

    def qb_rating(self) -> float:
        pass

    def st_rating(self) -> float:
        pass

