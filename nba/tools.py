


import json


def open_json(file_name: str) -> dict:
    with open(file_name) as file:
        data = json.load(file)
        return data

def save_json(file_name: str, data: dict) -> None:
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print('Data has been saved to ' + file_name)

        

