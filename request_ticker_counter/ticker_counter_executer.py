import os
from datetime import datetime, timedelta
import time
import schedule
import config
import request_ticker_counter.ticker_counter
from request_ticker_counter.ticker_counter_commons import *


def get_path_to_daily_result():
    return f"{config.SAVING_FOLDER}/daily_results"


def save_result(result, date_str):
    path_to_daily_results = get_path_to_daily_result()
    file_path = f"{path_to_daily_results}/{date_str}.json"

    if not os.path.exists(path_to_daily_results):
        os.makedirs(path_to_daily_results)

    with open(file_path, "w") as json_file:
        json.dump(result, json_file, indent=4)


def check_if_result_exists(date_str):
    path_to_daily_results = get_path_to_daily_result()
    file_path = f"{path_to_daily_results}/{date_str}.json"
    return os.path.exists(file_path)


def read_result_from_file(date_str):
    path_to_daily_results = get_path_to_daily_result()
    file_path = f"{path_to_daily_results}/{date_str}.json"
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def get_batch_for_specific_date(date_str):
    if check_if_result_exists(date_str):
        result = read_result_from_file(date_str)
        logger.info(f"data exists for: {date_str}")
        logger.info(f"result: {result}")
        return result
    else:
        calculated_result =  request_ticker_counter.ticker_counter.main_execution(date_str)
        logger.info(f"data not exist for date: {date_str}")
        logger.info(f"calculated result: {calculated_result}")
        logger.info(f"save result to file")
        save_result(calculated_result, date_str)
        return calculated_result


def get_yesterday_str():
    today = datetime.today()
    yesterday = today - timedelta(days=1)  # Subtract 1 day
    yesterday_str = yesterday.strftime("%Y-%m-%d")  # Format as string
    return yesterday_str


def main():
    yesterday_str = get_yesterday_str()
    logger.info(f"execute counter for day: {yesterday_str}")
    get_batch_for_specific_date(yesterday_str)



