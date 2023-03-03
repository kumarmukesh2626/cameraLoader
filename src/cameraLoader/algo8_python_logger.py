# from cmreslogging.handlers import CMRESHandler
import logging
import configparser
import sys
from datetime import datetime
DEFAULT_MSG = ""
logging.basicConfig(filename="log_files/"+"Log_"+str(datetime.now().date())+".log",
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')
# logging.basicConfig(filename = 'test5.log',level = logging.INFO,format = '%(asctime)s %(message)s')


def get_level(level):
    if level == "DEBUG":
        return logging.DEBUG
    if level == "INFO":
        return logging.INFO
    if level == "WARNING":
        return logging.WARNING
    if level == "ERROR":
        return logging.ERROR


# def get_elk_credentials():
#     # reading configuration file
#     config_file = configparser.ConfigParser()
#     config_file.read("config.ini")
#     return config_file["elk_credentials"]


def get_logger_config():
    # reading configuration file
    config_file = configparser.ConfigParser()
    config_file.read("config.ini")
    return config_file["algo8_python_logger"]


class Create_Custom_Logger:
    def __init__(self, logger=logging.getLogger()):
        self.logger = logger

    def debug(self, data):
        message = data.pop("message", DEFAULT_MSG)
        self.logger.debug(message, extra=data)

    def info(self, data):
        message = data.pop("message", DEFAULT_MSG)
        self.logger.info(message, extra=data)

    def warning(self, data):
        message = data.pop("message", DEFAULT_MSG)
        self.logger.warning(message, extra=data)

    def error(self, data):
        message = data.pop("message", DEFAULT_MSG)
        self.logger.error(message, extra=data)


# def elk_aws_logger(opts):
#     """
#     ELK AWS Logger
#     """
#     index_name = str(opts["project"] + "_" + opts["module"] + "_" + opts["app_env"])
#     elk_credentials = get_elk_credentials()

#     # creating handler
#     handler = CMRESHandler(
#         hosts=[
#             {
#                 "host": elk_credentials["elk_host"],
#                 "port": 443,
#             }
#         ],
#         auth_type=CMRESHandler.AuthType.AWS_SIGNED_AUTH,
#         aws_access_key=elk_credentials["aws_access_key"],
#         aws_secret_key=elk_credentials["aws_secret_key"],
#         aws_region=elk_credentials["aws_region"],
#         es_index_name=index_name,
#         use_ssl=True,
#         index_name_frequency=CMRESHandler.IndexNameFrequency.MONTHLY,
#         es_additional_fields={
#             "Project": opts["project"],
#             "Module": opts["module"],
#             "Environment": opts["app_env"],
#         },
#     )
def logging1(opts):
    logger = logging.getLogger(opts["logger_name"])
    logger.setLevel(opts["level"])

    if len(logger.handlers) > 0:
        raise Exception("More than one logger created")
        # python_logger.handlers.pop()
    logger.addHandler(handler)

    my_logger = Create_Custom_Logger(logger)
    return (index_name, my_logger)


def create_algo8_python_logger():
    logger_config = get_logger_config()

    project = str(logger_config["project"]).lower()
    module = str(logger_config["module"]).lower()
    app_env = str(logger_config["env"]).lower() or str("dev")
    log_level = str(logger_config["log_level"]) or str("INFO")
    display_in_console = str(logger_config["console"]) or str("True")

    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        raise Exception('level must be one of "DEBUG", "INFO", "WARNING","ERROR"')

    if app_env not in ["local", "dev", "test", "prod"]:
        raise Exception("Please provide a valid env")

    logger_name = "algo8_python_logger_v1"
    level = get_level(log_level)

    if display_in_console in ["YES", "Y", True, "True"]:
        python_logger = logging.getLogger(logger_name)
        python_logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        python_logger.addHandler(handler)
        print("Logging to Console")
        return python_logger

    if not project:
        raise Exception("Please provide a valid project name")
    if not module:
        raise Exception("Please provide a valid module name")

    # Future: Include APP_VERSION, OS

    opts = {
        "logger_name": logger_name,
        "level": level,
        "project": project,
        "module": log,
        "app_env": app_env,
    }

    (index_name, my_logger) = logging(opts)
#     print(f"Sending logs to ELK at index: {index_name}")
    return my_logger


# Initiated Once
algo8_python_logger = create_algo8_python_logger()
