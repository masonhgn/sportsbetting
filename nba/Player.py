




class Player:
    def __init__(self, player_id: int, full_name: str) -> None:
        self.id = player_id
        self.full_name = full_name

        self.basic_stats = {}
        self.calculated_stats = {}


    def add_game(season: int, game_id: str, regular_season: bool, stats_dict: dict) -> None:
        '''adds a single game's worth of stats for the player'''
        if not season in self.basic_stats: self.basic_stats[season] = {}
        game_type = 'regular_season' if regular_season else 'playoffs'
        self.basic_stats[season][game_type][game_id] = stats_dict