import sys
import time
import logging


def Logger(config, handler=None, level=None):
    identifier = None

    if hasattr(config, 'service_instance'):
        identifier = config.service_instance + '-' + config.environment
    elif hasattr(config, 'service_name'):
        identifier = config.service_name + '-' + config.environment
    else:
        identifier = config.environment

    if level not in [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]:
        level = logging.INFO

    logging.Formatter.converter = time.gmtime
    defaultHandler = logging.StreamHandler(sys.stdout)
    defaultHandler.setLevel(level)

    log = logging.getLogger(identifier)
    log.setLevel(level)

    # Clear any hanging/zombie handlers
    log.handlers = []

    defaultHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    log.addHandler(defaultHandler)

    return log
