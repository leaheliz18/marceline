import json

def load_reaction_ids(path="reaction_config.json"):
    """load message_ids from a json config file"""
    try:
        with open(path, "r") as f:
            return json.load(f).get("message_ids", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_reaction_ids(ids, path="reaction_config.json"):
    """save message_ids to a json config file"""
    with open(path, "w") as f:
        json.dump({"message_ids": ids}, f)
