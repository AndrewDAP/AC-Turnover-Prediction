"""Mapping Loader helper function
"""

import json


def load_json_mapping_to_dict(json_file_path):
    """Loads a json mapping and returns a dict

    Args:
        json_file_path (str): the json file path

    Returns:
        dict: the mapping in dict format
    """
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        # Load JSON and remove double quotes from values
        data_dict = {
            int(key): value.strip('"') for key, value in json.load(json_file).items()
        }
    return data_dict
