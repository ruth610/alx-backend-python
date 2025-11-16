def access_nested_map(nested_map,path):
    value = nested_map

    for key in path:
        value = value[key]
    
    return value
