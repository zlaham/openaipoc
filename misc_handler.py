def read_configuration():
    file_path = './configuration.txt'
    config_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        config_str = file.read()  # Read the entire content of the file
        
    # Split the string into individual key-value pairs
    config_items = config_str.strip().split(';')
    
    for item in config_items:
        if item:  # Ensure the item is not empty (to avoid trailing semicolon issues)
            key, value = item.split('=')
            config_dict[key.strip()] = value.strip()
    
    return config_dict

def parse_and_filter_configuration(keys_to_keep):
    config_dict = read_configuration()
    filtered_dict = {key: value for key, value in config_dict.items() if key in keys_to_keep}
    return filtered_dict