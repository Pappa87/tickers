from logbook import Logger, FileHandler, StreamHandler
import sys


if 'logger' not in locals():
    log_format = "{record.time:%Y-%m-%d %H:%M:%S} - {record.level_name} - {record.message}"

    console_handler = StreamHandler(sys.stdout, level="INFO", format_string=log_format)
    console_handler.push_application()
    logger = Logger("logger")
