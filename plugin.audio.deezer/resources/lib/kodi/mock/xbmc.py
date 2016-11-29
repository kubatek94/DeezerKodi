import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

LOGDEBUG = logging.DEBUG
LOGERROR = logging.ERROR
LOGFATAL = logging.FATAL
LOGINFO = logging.INFO
LOGNONE = logging.NOTSET
LOGNOTICE = logging.INFO
LOGSEVERE = logging.CRITICAL
LOGWARNING = logging.WARNING


def log(msg, level=LOGNOTICE):
    logging.log(level, msg)

def executebuiltin(command):
    log("Execute built-in: %s" % command)