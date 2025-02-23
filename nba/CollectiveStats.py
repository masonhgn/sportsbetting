


class CollectiveStats:
    def __init__(self):
        self.league_stats = {}
        self.team_stats = {}



    def add_league_stat(self, season: int, regular_season: bool, game_id: str, stat_name: str, stat: float) -> None:
        '''adds a specific stat to the league wide stats for that season for that game'''
        if not season in self.league_stats:
            self.league_stats[season] = {'regular_season': {}, 'playoffs': {}}

        game_type = 'regular_season' if regular_season else 'playoffs'

        if game_id not in self.league_stats[season][game_type]:
            self.league_stats[season][game_type][game_id] = {}

        if stat_name not in self.league_stats[season][game_type][game_id]:
            self.league_stats[season][game_type][game_id][stat_name] = []
        
        self.league_stats[season][game_type][game_id][stat_name].append(stat)




    def add_team_stat(self, season: int, regular_season: bool, game_id: str, team_id: str, stat_name: str, stat: float) -> None:
        '''adds a specific stat to the team wide stats for that season for that game'''
        if not season in self.team_stats:
            self.team_stats[season] = {'regular_season': {}, 'playoffs': {}}

        game_type = 'regular_season' if regular_season else 'playoffs'

        if game_id not in self.team_stats[season][game_type]:
            self.team_stats[season][game_type][game_id] = {}

        if team_id not in self.team_stats[season][game_type][game_id]:
            self.team_stats[season][game_type][game_id][team_id] = {}

        if stat_name not in self.team_stats[season][game_type][game_id][team_id]:
            self.team_stats[season][game_type][game_id][team_id][stat_name] = []

        self.team_stats[season][game_type][game_id][team_id][stat_name].append(stat)