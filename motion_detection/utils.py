import yaml

def load_config():
    with open('../motion_detection/config.yml', 'r') as file:
        return yaml.safe_load(file)