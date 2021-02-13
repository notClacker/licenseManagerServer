import logging
from logging.handlers import RotatingFileHandler

# CFG
g_log_file_path = u'logs/'

#g_logging_console = logging.WARNING
g_logging_console = logging.DEBUG
g_log_console_format = "[%(levelname)s]: %(message)s"

g_log_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"

error_files_count = 30
error_file_bytes = 10 * 1024 * 1024

def setup_logging():
    # Main logger
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(g_logging_console)
    console_handler.setFormatter(logging.Formatter(g_log_console_format))

    exp_file_handler = RotatingFileHandler('{}debug.log'.format(g_log_file_path), maxBytes=1024*1024, backupCount=1)
    exp_file_handler.setLevel(logging.DEBUG)
    exp_file_handler.setFormatter(logging.Formatter(g_log_file_format))

    exp_errors_file_handler = RotatingFileHandler('{}warning.log'.format(g_log_file_path), maxBytes=error_file_bytes, backupCount=error_files_count)
    exp_errors_file_handler.setLevel(logging.WARNING)
    exp_errors_file_handler.setFormatter(logging.Formatter(g_log_file_format))

    main_logger.addHandler(console_handler)
    main_logger.addHandler(exp_file_handler)
    main_logger.addHandler(exp_errors_file_handler)
    return main_logger

logger = setup_logging()
