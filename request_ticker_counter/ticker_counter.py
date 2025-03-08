import os
import re

from ticker_downloader import get_tickers
from json_parse_approach.common import logger
from ticker_counter_file_manipulation import *
from ticker_counter_commons import *
from ticker_counter_loggers import *

DOWNLOAD_FOLDER = "C:\\tmp\\ticker_test_data"
tickers = get_tickers()

cmpny_names = [ticker.name for ticker in tickers]


def asses_download_batch(download_folder):
    global tickers

    downloaded_jsons = list_files(download_folder)
    result = {}
    for json_path in downloaded_jsons:

        text = open_file(json_path)
        cmpny_name_matches = search_for_company_names(text)
        symbol_matches = search_for_tickers(text)
        match_report = MatchReport(json_path, cmpny_name_matches, symbol_matches)

        result = add_matches_to_report(result, match_report.symbol_matches)
        result = add_matches_to_report(result, match_report.cmpny_name_matches)

        log_matches(match_report, result)
        log_matches_text_environment(json_path, match_report.symbol_matches, tickers)
        # (json_path, match_report.cmpny_name_matches)

    log_final_result(result)
    return result


def log_final_result(result):
    sorted_result = sorted(result.items(), key=lambda x: x[1],reverse=True)
    logger.info(f"final_result: {sorted_result}")


def add_matches_to_report(current_result: dict, match_dict: dict):
    result = current_result
    expressions = match_dict.keys()

    for expression in expressions:
        if expression not in result.keys():
            result[expression] = match_dict[expression]
        else:
            result[expression] = result[expression] + match_dict[expression]

    return result


def search_for_company_names(searchable_text):
    global tickers
    result = {}
    for ticker in tickers:
        ticker_name = ticker.name
        simplified_ticker = simplify_ticker_name(ticker_name)

        matches = search_for_expression(searchable_text, simplified_ticker)
        if len(matches) > 0:
            result[ticker_name] = len(matches)
    return result


def search_for_tickers(searchable_text):
    global tickers

    filtered_tickers = [ticker for ticker in tickers if len(ticker.symbol) > 3]
    result = {}
    for ticker in filtered_tickers:
        name_of_ticker = ticker.name
        symbol_of_ticker = ticker.symbol
        matches = search_for_expression(searchable_text, symbol_of_ticker)
        if len(matches) > 0:
            result[name_of_ticker] = len(matches)
    return result


asses_download_batch("./saving_folder/2025_03_07__17_05_47")

# print(search_for_expression(""" Nvidia shareholders giving away sh""", "Nvidia"))