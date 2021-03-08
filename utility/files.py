# File methods
import json

def load_json(filename: str) -> dict:
    return json.load(open(filename))