import json

def loadConfig(config_file: str) -> dict:
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def loadItem(config_file: str, item: str) -> str:
    config = loadConfig(config_file)
    return config.get(item, "")