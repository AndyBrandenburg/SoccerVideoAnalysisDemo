import json
def load_tracking_data(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

