
from collections import defaultdict

class CollectiveStats:
    def __init__(self):
        self.league_stats = {}
        self.team_stats = {}



    def add_league_stat(self, season: int, regular_season: bool, game_id: str, stat_name: str, stat: float) -> None:

        if season not in self.league_stats:
            self.league_stats[season] = {'regular_season': {}, 'playoffs': {}}

        game_type = 'regular_season' if regular_season else 'playoffs'
        season_games = self.league_stats[season][game_type]


        previous_game_id = next(reversed(season_games), None)


        if game_id not in season_games:
            if previous_game_id:
            
                season_games[game_id] = {stat: list(season_games[previous_game_id].get(stat, [])) for stat in season_games[previous_game_id]}
            else:
             
                season_games[game_id] = defaultdict(list)

       
        season_games[game_id][stat_name].append(stat)




    def add_team_stat(self, season: int, regular_season: bool, game_id: str, team_id: str, stat_name: str, stat: float) -> None:
     
        if season not in self.team_stats:
            self.team_stats[season] = {'regular_season': {}, 'playoffs': {}}

        game_type = 'regular_season' if regular_season else 'playoffs'
        season_games = self.team_stats[season][game_type]

        if game_id not in season_games:
            season_games[game_id] = {}

        if team_id not in season_games[game_id]:
            previous_game_id = next(reversed(season_games), None)
            if previous_game_id and team_id in season_games[previous_game_id]:
        
                season_games[game_id][team_id] = {stat: list(season_games[previous_game_id][team_id].get(stat, [])) for stat in season_games[previous_game_id][team_id]}
            else:
    
                season_games[game_id][team_id] = defaultdict(list)


        season_games[game_id][team_id][stat_name].append(stat)




    def get_stats_by_game(self, season: int, game_id: str, regular_season: bool) -> dict:
        game_type = 'regular_season' if regular_season else 'playoffs'
        stats = {
            'league_stats': self.league_stats.get(season, {}).get(game_type, {}).get(game_id, {}),
            'team_stats': self.team_stats.get(season, {}).get(game_type, {}).get(game_id, {})
        }
        return stats