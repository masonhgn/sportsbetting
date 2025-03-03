

import json
from collections import defaultdict
from tools import time_to_minutes

class Player:
    def __init__(self, player_id: int = None, full_name: str = None) -> None:

        self.id = player_id
        self.full_name = full_name

        self.basic_stats = {}
        self.compounded_stats = {}
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



    def update_compounded_stats(self, season: int, game_id: str, regular_season: bool, stats_dict: dict) -> None:
        if season not in self.compounded_stats:
            self.compounded_stats[season] = {'regular_season': {}, 'playoffs': {}}
        
        game_type = 'regular_season' if regular_season else 'playoffs'
        season_games = self.compounded_stats[season][game_type]
        
        previous_game_id = next(reversed(season_games), None)
        
        if game_id not in season_games:
            if previous_game_id:
                season_games[game_id] = {stat: list(season_games[previous_game_id].get(stat, [])) for stat in season_games[previous_game_id]}
            else:
                season_games[game_id] = defaultdict(list)

        for stat_name, stat_value in stats_dict.items():
            if stat_name == 'min': stat_value = time_to_minutes(stat_value)
            if isinstance(stat_value, (int, float)):
                season_games[game_id][stat_name].append(stat_value)






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
                        if stat == 'min': value = time_to_minutes(value)
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


    


    @classmethod
    def calculate_uper(self,
        lgTRB: float, #league total rebounds
        lgORB: float, #league offensive rebounds
        lgPTS: float, #league total points
        lgFGA: float, #league field goal attempts
        lgTO: float, #league turnovers
        lgFTA: float, #league free throw attempts
        lgAST: float, #league assists
        lgFT: float, #league free throws
        lgFG: float, #league field goals
        lgPF: float, #personal fouls
        tmAST: float, #team assists
        tmFG: float, #team field goals
        mins: float, #minutes played
        ast: float, #assists
        fg: float, #field goals
        fga: float, #field goal attempts
        to: float, #turnovers 
        trb: float, #total rebounds
        orb: float, #offensive rebounds
        stl: float, #steals
        blk: float, #blocks
        fta: float, #free throw attempts
        ft: float, #free throws
        tp: float, #three pointers
        pf: float, #personal fouls
    ) -> float:

        if lgFG == 0 or lgFT == 0 or lgFGA == 0 or lgFTA == 0 or lgPF == 0 or mins == 0 or tmFG == 0:
                return None #prevent division by 0


        try:
            factor = float(2/3) - ((0.5 * (lgAST/lgFG)) / 2 * (lgFG/lgFT))
            vop = lgPTS/(lgFGA-lgORB+lgTO+(0.44*lgFTA))
            drbp = (lgTRB-lgORB)/lgTRB

            uper = 1/mins * (tp + (float(2/3)*ast) \
                    + ((2-(factor*tmAST/tmFG))*fg)    \
                    + (0.5 * ft * (2-(tmAST/tmFG/3))) \
                    - (vop * to) - ((vop * drbp) * (fga-fg)) \
                    - (vop * 0.44 * (0.44 + (0.56 * drbp)) * (fta - ft)) \
                    + (vop * (1-drbp) * (trb - orb)) \
                    + (vop * drbp * orb) + (vop * stl) \
                    + (vop * drbp * blk) \
                    - (pf * ((lgFT/lgPF) - (0.44 * (lgFTA/lgPF) * vop))))
            
        except ZeroDivisionError as e:
            variables = {
                "lgTRB": lgTRB, "lgORB": lgORB, "lgPTS": lgPTS, "lgFGA": lgFGA, "lgTO": lgTO, "lgFTA": lgFTA,
                "lgAST": lgAST, "lgFT": lgFT, "lgFG": lgFG, "lgPF": lgPF, "tmAST": tmAST, "tmFG": tmFG,
                "mins": mins, "ast": ast, "fg": fg, "fga": fga, "to": to, "trb": trb, "orb": orb,
                "stl": stl, "blk": blk, "fta": fta, "ft": ft, "tp": tp, "pf": pf
            }
            for var, value in variables.items():
                if value == 0:
                    print(f" {var} = {value} (Possible issue!)")
            exit()

    def calculate_per(self, uper: float, lgPace: float, tmPace: float, lgUper: float) -> float:
        per = uper * (lgPace / tmPace) * 15/lgUper
        return per
            