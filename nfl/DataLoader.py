import requests
from player import Player


MIN_YEAR, MAX_YEAR = 1970, 2024


class DataLoader:

    def __init__(self):
        self.all_teams = ['BUF', 'MIA', 'NYJ', 'NE', 'BAL', 'PIT', 'CIN', 'CLE',
                          'HOU', 'IND', 'JAX', 'TEN', 'KC', 'LAC', 'DEN', 'LV', 
                          'PHI', 'WSH', 'DAL', 'NYG', 'DET', 'MIN', 'GB', 'CHI', 
                          'TB', 'ATL', 'NO', 'CAR', 'LAR', 'SEA', 'ARI', 'SF']

        self.apikey = '6d8471b900msh64f82e14a3ea8c4p1e6eedjsn363222b8f5fe'


    def get_team_schedule(self, team: str, season: int, include_preseason: bool = False) -> list:
        """gets the schedule for a specific team for a specific season"""
        #1 api call
        assert team in self.all_teams and MIN_YEAR <= season <= MAX_YEAR

        schedule = []
        url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLTeamSchedule"

        querystring = {"teamAbv":team,"season":season}

        headers = {
            "x-rapidapi-key": self.apikey,
            "x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        #print(response.json())
        response = response.json()['body']['schedule']

        for game in response:
            if not include_preseason and game['seasonType'] == 'Preseason': continue #don't include preseason games
            schedule.append(game['gameID'])
        
        return schedule




    def get_gameids_by_season(self, season: int) -> list:
        """gets IDs of all games for a particular season and returns them in a list"""
        #32 api calls
        assert MIN_YEAR <= season <= MAX_YEAR

        total_games = []

        for team in self.all_teams:
            all_games = self.get_team_schedule(team, season)

            for game in all_games:
                if game not in total_games:
                    total_games.append(game)


    def get_boxscore(self, game_id: str) -> dict:
        """gets the boxscore for a single game"""
        #1 api call
        url = "https://tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com/getNFLBoxScore"

        querystring = {"gameID":game_id}

        headers = {
            "x-rapidapi-key": self.apikey,
            "x-rapidapi-host": "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        response = response.json()

        return response 

        
    def get_all_boxscores_by_season(self, gameid_list: list[str]) -> dict:
        """gets boxscores of all games in a list of game ids"""
        #len(gameid_list) api calls
        assert len(gameid_list)
        
        boxscores = {}

        for index, game_id in enumerate(gameid_list):
            boxscores[game_id] = get_boxscore(game_id)
            print('fetched ' + str(index+1) + ' of ' + str(len(gameid_list)) + ' games...')

        return boxscores



    def sort_boxscores_by_player(self, season: int, boxscores: dict) -> dict:
        """takes boxscores and creates a dict where k=player_id, v= a list of dicts, each dict containing the stats of a single game"""
        """basically makes a directory of players seasons"""
        all_players = {}
        for game_id in boxscores.keys():
            single_game = boxscores[game_id]['body']['playerStats']
            for player_id, player_stat in single_game.items():
                if player_id not in all_players: all_players[player_id] = []
                all_players[player_id].append(player_stat)

        return all_players



    def record_player_season_stats(self, player_id: str, all_players_dict: dict, season: int, existing_player: Player = None) -> Player:
        assert player_id in all_players_dict.keys() and len(list(all_players_dict[player_id])) >= 1
        assert MIN_YEAR <= season <= MAX_YEAR
        player_name = all_players_dict[player_id][0]['longName']
        print(player_name)
        
        player = Player(player_id, player_name) if not existing_player else existing_player
        
        entire_season = all_players_dict[player_id]

        for game in entire_season:
            player.total_games_recorded += 1
            if 'snapCounts' in game:
                sc = game['snapCounts']
                for stat_name in ['offSnapPct','offSnap','defSnapPct','defSnap','stSnapPct','stSnap']:
                    if stat_name in sc:
                        player.add_stat(season, stat_name, float(sc[stat_name]))

            if 'Rushing' in game:
                rs = game['Rushing']
                for stat_name in ['rushAvg','rushYds','carries','rushTD']:
                    if stat_name in rs:
                        player.add_stat(season, stat_name, float(rs[stat_name]))

            if 'Receiving' in game:
                rc = game['Receiving']
                for stat_name in ['receptions','recYds','recAvg','targets']:
                    if stat_name in rc:
                        player.add_stat(season, stat_name, float(rc[stat_name]))

            if 'Passing' in game:
                ps = game['Passing']
                for stat_name in ['qbr','rtg','passAttempts','passAvg','passTD','passYds','int','passCompletions']:
                    if stat_name in ps:
                        player.add_stat(season, stat_name, float(ps[stat_name]))

            if 'Defense' in game:
                df = game['Defense']
                for stat_name in ['totalTackles','soloTackles','forcedFumbles','sacks','defensiveInterceptions','passDeflections']:
                    if stat_name in df:
                        player.add_stat(season, stat_name, float(df[stat_name]))

        return player
    


    def update_player_dict_by_season(self, season: int, players_dict: dict) -> None:
        """gets player stats for a whole season, updating the players_dict dictionary passed in with the new season of stats for each player"""
        game_ids = self.get_gameids_by_season(season)
        boxscores = self.get_all_boxscores_by_season(game_ids)
        player_stats_dict = self.sort_boxscores_by_player(season, boxscores)
        
        for player_id in player_stats_dict.keys():

            #try to index player in dictionary if possible
            cur_player = None if player_id not in players_dict else players_dict[player_id]

            #update player in dictionary
            players_dict[player_id] = self.record_player_season_stats(player_id, player_stats_dict, season, cur_player)



    def print_hello(self):
        print('hello!')



