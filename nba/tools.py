


import json
from datetime import date

def open_json(file_name: str) -> dict:
    with open(file_name) as file:
        data = json.load(file)
        return data

def save_json(file_name: str, data: dict) -> None:
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print('Data has been saved to ' + file_name)



def convert_to_datetime(date_str: str) -> date:
    '''"start": "2015-10-03T02:30:00.000Z" -> datetime.date'''
    return date.fromisoformat(date_str[:10])

def compare_dates(date1: str, date2: str) -> bool:
    '''returns True if date1 is strictly after date2'''
    return convert_to_datetime(date1) > convert_to_datetime(date2)




        

