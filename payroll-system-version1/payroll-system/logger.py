#!/usr/bin/python
#coding: utf-8

import logging
import logging.handlers

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

rh=logging.handlers.TimedRotatingFileHandler('logger.log','D')
fm=logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
rh.setFormatter(fm)
logger.addHandler(rh)

if __name__ == "__main__":
    debug=logger.debug
    info=logger.info
    warn=logger.warn
    error=logger.error
    critical=logger.critical

    info("testlog1")
    warn("warn you %s","costaxu")
    critical("it is critical")