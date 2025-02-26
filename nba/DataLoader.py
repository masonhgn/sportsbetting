
import json
from Player import Player
from CollectiveStats import CollectiveStats




class DataLoader:

    '''this class is meant to create, store and load Player objects and CollectiveStats objects. It stores everything in JSON format, and is 
    meant to be a one stop shop for aggregating all of the necessary data for our models in a way that's much easier to process than the API responses.'''

    def __init__(self):
        self.players = {}
        self.collective_stats = {}





    def create_player_stats(self) -> None:
        '''opens game JSON files (/games directory) and creates Player objects'''
        pass



    def load_player_stats(self, file_name: str) -> dict:
        '''loads player stats from JSON Player objects'''
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
            
            players = {player_id: Player.from_dict(player_data) for player_id, player_data in data.items()}
            self.players = players

        except FileNotFoundError:
            print(f"error: the file '{file_name}' does not exist")
            return {}
        except json.JSONDecodeError:
            print(f"error: failed to decode JSON from the file '{file_name}'")
            return {}


    def load_collective_stats(self) -> None:
        pass

    