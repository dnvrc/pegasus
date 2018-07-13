import sys
import time
import logging

from pythonjsonlogger import jsonlogger

JSON_FORMAT = '%(asctime)s %(filename)s %(name)s %(levelname)s %(message)s'
STAD_FORMAT = '%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s'


def Logger(config, handler=None, level=None, disabled=False):
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

    if disabled:
        defaultHandler.setFormatter(logging.Formatter(STAD_FORMAT))
        log.addHandler(defaultHandler)
        return log

    defaultHandler.setFormatter(jsonlogger.JsonFormatter(JSON_FORMAT))
    log.addHandler(defaultHandler)

    return log
