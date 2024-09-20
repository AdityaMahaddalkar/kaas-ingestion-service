import yaml


class Config:
    def __init__(self):
        with open('config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

    def get_config(self):
        return self.config
