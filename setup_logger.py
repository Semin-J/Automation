import logging

formatter = logging.Formatter(fmt = '%(asctime)s.%(msecs)03d|%(levelname)s|%(module)s|%(message)s',
                              datefmt = '%Y-%m-%d@%H:%M:%S')


# To set up multiple loggers
def setup_logger(name, log_path, level = logging.INFO):

  handler = logging.FileHandler(log_path)
  handler.setFormatter(formatter)

  logger = logging.getLogger(name)
  logger.setLevel(level)
  logger.addHandler(handler)

  return logger
