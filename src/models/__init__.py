import dotmap


class Base(object):
    def __init__(self, config, connection, model):
        self.config = config
        self.connection = connection
        self.model = model

    def clean_print(self, data):
        print('')
        print(data)
        print('')


class Model(dotmap.DotMap):
    pass
