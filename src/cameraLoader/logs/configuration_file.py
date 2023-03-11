
"""
Created on Tue Jul 13 14:33:39 2021

@author: Hardik Seth | Algo8.ai

"""

import logging
import logging.handlers
from datetime import datetime
import os
import sys
import configparser

def get_logger_config():
    try:
        # reading configuration file
        config_file = configparser.ConfigParser()
        config_file.read("config/common_config.ini")
        return True,config_file["LOGS"]
    except:
        False, "failed to read config file"

# function to provide configuration of logging
# function to provide configuration of logging
def logger_handle(path):
    logger = logging.getLogger(__name__)

    # check if log handle already exist in the progam if yes no need to follow configuration. Prevents multiple instance of same log.
    if len(logger.handlers) == 0:
        logger.setLevel(logging.INFO)
        # line will create a Roatating Log which gets appended untill the size limit defined is filled.
        # max log size can be 20mb
        path = os.path.join(path, "App_" + str(datetime.now().date()) + ".log")
        print(path, logging.INFO)
        handler = logging.handlers.RotatingFileHandler(path, mode='a', maxBytes=1024 * 1024 * 20, backupCount=2,
                                                       encoding=None, delay=0)
        handler.setLevel(logging.INFO)
        # setting a fixed format for the logs
        formatter = logging.Formatter('{Log Time:%(asctime)s, Type:%(levelname)s, %(message)s}')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # return above mentioned log var with all configurations
    return logger

# function to generate log based on status and send the success status log  file 
def success_log(status_code,message,function_name):
    message_final = "Message:" + message + ", Status Code: " + str(status_code)+ ", Function Name: " + str(function_name)
    l.info(message_final)

# function to generate log based on status and send fail status the log file
def error_log(status_code,message,function_name):
    message_final = "Message:" + message + ", Status Code: " + str(status_code)+ ", Function Name: " + str(function_name)
    l.error(message_final)


status,conf = get_logger_config()  
log_path = conf["log_path"]
log_console = conf["display_in_console"]
l = logger_handle(log_path)
# error_log("200","function called successfully","main.dev")