import logging

import yaml


class Config:
    def __init__(self):
        with open('config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        logging.basicConfig(
            level=self._get_logging_level()
        )

    def get_config(self):
        return self.config

    def _get_logging_level(self):
        assert 'logging' in self.config and 'level' in self.config['logging'], 'Logging config not set for the app'

        level = None

        if self.config['logging']['level'] == 'INFO':
            return logging.INFO
        else:
            return logging.ERROR
