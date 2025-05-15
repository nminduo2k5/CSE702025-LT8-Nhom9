import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def Logger_Days(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                    datefmt='%Y/%m/%d %H:%M:%S') # %I:%M:%S %p AM|PM format
    # handler = TimedRotatingFileHandler(filename = '%s.log' %(file_name), when="midnight", backupCount=30)
    # handler.suffix = "%Y%m%d"
    handler = TimedRotatingFileHandler(filename = '%s.log' %(file_name), when="D", backupCount=20)
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.INFO)

    # console printer
    # screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
    handler.setFormatter(formatter)
    log_obj.addHandler(handler)

    log_obj.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    log_obj.info("Logger object created successfully..")
    return log_obj

def Logger_maxBytes(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                    datefmt='%Y/%m/%d %H:%M:%S') # %I:%M:%S %p AM|PM format
    handler = RotatingFileHandler(filename = '%s.log' %(file_name), mode = 'a', maxBytes=5, backupCount=0, 
                                  encoding='utf-8', delay=0)
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.INFO)

    # console printer
    # screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
    handler.setFormatter(formatter)
    log_obj.addHandler(handler)

    log_obj.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    log_obj.info("Logger object created successfully..")
    return log_obj