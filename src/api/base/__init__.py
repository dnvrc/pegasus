import os
import quandl

class APIBase(object):
    def __init__(self, config):
        self.config = config
