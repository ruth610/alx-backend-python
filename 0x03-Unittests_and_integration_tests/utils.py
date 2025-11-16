import requests


def access_nested_map(nested_map,path):
    value = nested_map

    for key in path:
        if not isinstance(value,dict):
            raise KeyError(key)
        value = value[key]
    
    return value


def get_json(url):
    response = requests.get(url)
    return response.json()