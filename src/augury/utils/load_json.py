import json

def load_json(path: str):
    with open(path, "r") as f:
        json_data = json.load(f)

        return json_data