import logging

logger = logging.getLogger("lama")

class Filter(logging.Filter):
    def warningfilter(self, record):
        return record.levelno <= logging.INFO

handler_for_exceptions = logging.FileHandler(filename="errors.log", mode='w')
handler_for_exceptions.addFilter(Filter())
handler_for_exceptions.setFormatter(logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s"))

logger.addHandler(handler_for_exceptions)