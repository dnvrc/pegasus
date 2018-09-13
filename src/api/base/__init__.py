import os
import quandl

class APIBase(object):
    def __init__(self, config):
        self.config = config

        # Configure needed API keys here
        quandl.ApiConfig.api_key = os.getenv('QUANDL_API_KEY', None)
