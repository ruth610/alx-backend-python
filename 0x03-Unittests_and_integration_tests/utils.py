import requests


def access_nested_map(nested_map, path):
    value = nested_map

    for key in path:
        if not isinstance(value, dict):
            raise KeyError(key)
        value = value[key]

    return value


def get_json(url):
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Cache the result of a method without arguments."""
    attr_name = "_memoized_" + fn.__name__

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return wrapper
