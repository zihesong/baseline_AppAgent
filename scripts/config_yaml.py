import os
import yaml


def load_config(config_path="./config.yaml",api_key_path="./api_key.yaml"):
    configs = dict(os.environ)
    with open(config_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    configs.update(yaml_data)
    with open(api_key_path, "r") as file:
        api_key = yaml.safe_load(file)
    configs.update(api_key)
    return configs
