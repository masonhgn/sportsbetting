

import json
from collections import defaultdict

class Player:
    def __init__(self, player_id: int = None, full_name: str = None) -> None:

        self.id = player_id
        self.full_name = full_name

        self.basic_stats = {}
        self.calculated_stats = {}


    def add_game(self, season: int, game_id: str, regular_season: bool, stats_dict: dict) -> None:
        '''adds a single game's worth of stats for the player'''
        if not season in self.basic_stats: self.basic_stats[season] = {'regular_season': {}, 'playoffs': {}}
        game_type = 'regular_season' if regular_season else 'playoffs'
        self.basic_stats[season][game_type][game_id] = stats_dict


    def to_dict(self) -> dict:
        '''converts the Player object to a dict'''
        return {
            'id': self.id,
            'full_name': self.full_name,
            'basic_stats': self.basic_stats,
            'calculated_stats': self.calculated_stats
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        '''creates a Player object from a dict'''
        player = cls(player_id=data.get('id'), full_name=data.get('full_name'))
        player.basic_stats = data.get('basic_stats', {})
        player.calculated_stats = data.get('calculated_stats', {})
        return player

    def to_json(self) -> str:
        '''converts the Player object to a JSON string'''
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_json(cls, json_str: str) -> 'Player':
        '''creates a Player object from a JSON string'''
        data = json.loads(json_str)
        return cls.from_dict(data)


    def populate_calculated_stats(self, from_scratch: bool = False) -> None:

        if from_scratch:
            self.calculated_stats = {}

        career_totals = defaultdict(float)
        career_games_played = 0

        for season, season_data in self.basic_stats.items():
            if season not in self.calculated_stats:
                self.calculated_stats[season] = {'regular_season': {}, 'playoffs': {}}
        
            for game_type in ['regular_season', 'playoffs']:
                season_totals = defaultdict(float)
                games_played = 0

                for game_id, stats in season_data.get(game_type, {}).items():
                    if game_id in self.calculated_stats[season][game_type] and not from_scratch:
                        #skip if we already have the data
                        continue

                    games_played += 1
                    for stat, value in stats.items():
                        if isinstance(value, (int, float)):
                            season_totals[stat] += value
                            career_totals[stat] += value

                    career_games_played += 1

                    #get the stats for each game
                    self.calculated_stats[season][game_type][game_id] = {
                        'season_total': dict(season_totals),
                        #'career_total': dict(career_totals),
                        'season_average': {stat: total / games_played for stat, total in season_totals.items()},
                        #'career_average': {stat: total / career_games_played for stat, total in career_totals.items()}
                    }



    def pretty_print(self) -> None:
        '''Concise pretty print of player info, career stats, and latest season stats.'''
        print(f"\nPlayer ID: {self.id}")
        print(f"Full Name: {self.full_name}\n")

        # print("Career Stats:")
        # career_stats = defaultdict(float)
        # career_games_played = 0

        # for season, season_data in self.calculated_stats.items():
        #     for game_type, games in season_data.items():
        #         for game_id, stats in games.items():
        #             for stat, value in stats['career_total'].items():
        #                 career_stats[stat] = value
        #             career_games_played += 1

        # for stat, value in career_stats.items():
        #     print(f"  {stat.capitalize()}: {value}")

        print("\nLatest Season Stats:")
        latest_season = max(self.calculated_stats.keys(), default=None)
        if latest_season:
            latest_stats = defaultdict(float)
            games_played = 0

            for game_type, games in self.calculated_stats[latest_season].items():
                for game_id, stats in games.items():
                    for stat, value in stats['season_total'].items():
                        latest_stats[stat] = value
                    games_played += 1

            print(f"  Season {latest_season}:")
            for stat, value in latest_stats.items():
                print(f"    {stat.capitalize()}: {value}")

        print("\nEnd of Player Info\n")