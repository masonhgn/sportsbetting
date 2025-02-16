


import json


def open_json(file_name: str) -> dict:
    with open(file_name) as file:
        data = json.load(file)
        return data

def save_json(file_name: str, data: dict) -> None:
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print('Data has been saved to ' + file_name)

        

class Player:
    def __init__(self, player_id, player_name):
        self.total_games_recorded = 0

        self.player_id = player_id
        self.full_name = player_name


        #total plays
        self.total_offensive_snapPct = [] #player played in X% of total offensive snaps
        self.total_offensive_snaps = [] #number of offensive plays participated in
        self.total_defensive_snaps = [] #number of defensive plays participated in
        self.total_st_snaps = [] #number of special teams plays participated in



        #offensive stats, k="Rushing", "Receiving"
        self.total_rushAvg = []
        self.total_rushYds = []
        self.total_carries = []
        self.total_rushTD = []
        self.total_receptions = []
        self.total_recYds = []
        self.total_recAvg = []
        self.total_targets = []

        #quarterback, k="Passing"
        self.total_qbr = [] #quarterback rating
        self.total_rtg = [] #passer rating
        self.total_passAttempts = []
        self.total_passAvg = []
        self.total_passTD = []
        self.total_passYds = []
        self.total_int = []
        self.total_passCompletions = []


        #defensive stats k="Defense"
        self.total_totalTackles = []
        self.total_soloTackles = []
        self.total_forcedFumbles = []
        self.sacks = []
        self.total_defInterceptions = []
        self.total_passDeflections = []





