import logging, os, sys
from configparser import ConfigParser
from datetime import date

formatter = logging.Formatter( fmt="%(asctime)s.%(msecs)03d|%(levelname)s|%(module)s|%(message)s", datefmt="%Y-%m-%d@%H:%M:%S")


# To set up multiple loggers
def setup_logger(name, log_path, level=logging.INFO):

    handler = logging.FileHandler(log_path)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Create log files (Once created, append)
config = ConfigParser()
config.read(sys.argv[1])
batch_log_path = config["paths"]["script_log_path"]
today_pattern = date.today().strftime("%Y%m%d")

today_debug_log_path = os.path.join(batch_log_path, (today_pattern + "_Debug.log"))
today_info_error_log_path = os.path.join(batch_log_path, (today_pattern + "_Info_Error.log"))

# This debug_log is logging from DEBUG level to above (But us it for DEBUG level only)
debug_log = setup_logger("deb_log", today_debug_log_path, logging.DEBUG)

# This info_error_log is logging from INFO level to above (But use it for INFO, ERROR level only)
info_error_log = setup_logger("err_log", today_info_error_log_path, logging.INFO)
