from src.config.logger import Logger


class Config(object):
    def __init__(self):
        self.environment = 'local'
        self.logger = Logger(self, disabled=True)
