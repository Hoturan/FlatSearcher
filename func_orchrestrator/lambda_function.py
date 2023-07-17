import json
import tomli


def get_lambda_configs():
    """
    Opens the function_config.toml to gather the Locations to scrape from idealista
    """
    with open("function_config.toml", mode="rb") as config_file:
        config = tomli.load(config_file)
    return config
