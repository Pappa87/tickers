from datetime import datetime
from typing import Dict

from request_ticker_counter.ticker_downloader import get_tickers
from request_ticker_counter.ticker_counter_file_manipulation import *
from request_ticker_counter.ticker_counter_loggers import *

tickers = get_tickers()

cmpny_names = [ticker.name for ticker in tickers]


class ForumOccurrences:

    def __init__(self, json_path):
        self.forum_name = self.get_forum_name(json_path)
        self.occurrences = [json_path]

    def get_freshest_occurence(self, ):
        return max(self.occurrences, key=lambda occurrence: self.get_ts_from_json_path(occurrence))

    def get_ts_from_json_path(self, json_path):
        date_str = json_path.split("____")[-1][:-5].strip("_")
        date_format = "%Y_%m_%d__%H_%M_%S"
        parsed_date = datetime.strptime(date_str, date_format)
        return parsed_date

    def add_occurrence(self, json_path):
        self.occurrences.append(json_path)

    def get_num_of_occurrences(self):
        return len(self.occurrences)

    @staticmethod
    def get_forum_name(json_path):
        filename = os.path.basename(json_path)
        forum_name = filename.split("____")[0]
        return forum_name


class JsonManager:

    def __init__(self):
        self.json_paths: Dict[str, ForumOccurrences] = {}

    def add_json_path(self, json_path):
        forum_name = ForumOccurrences.get_forum_name(json_path)
        if forum_name in self.json_paths.keys():
            self.json_paths.get(forum_name).add_occurrence(json_path)
        else:
            self.json_paths[forum_name] = ForumOccurrences(json_path)

    def get_forum_ids(self):
        return self.json_paths.keys()

    def get_forum_occurrence(self, forum_id):
        return self.json_paths[forum_id]


def main_execution(date_str):
    json_manager = calculate_occurrences_for_specific_date(date_str)
    aggregated_report = searching_for_company_names(json_manager)
    log_final_result(aggregated_report)
    return aggregated_report


def searching_for_company_names(json_manager):
    forum_ids = json_manager.get_forum_ids()

    aggregated_report = {}
    current_state = 1

    logger.info("searching texts for company names")
    for forum_id in forum_ids:
        # logger.info(f"start to search for company names in {current_state}/{len(forum_ids)}")
        # current_state += 1

        forum_occurrence = json_manager.get_forum_occurrence(forum_id)

        freshest_occurrence = forum_occurrence.get_freshest_occurence()
        company_occurrences = calculate_match_report_for_file(freshest_occurrence).get_agg_report()

        num_of_occurrences = forum_occurrence.get_num_of_occurrences()
        multiplied_occ = multiple_cmpny_occurrences_with_forum_occurrences(company_occurrences, num_of_occurrences)

        aggregated_report = add_matches_to_report(aggregated_report, multiplied_occ)
    return aggregated_report


def multiple_cmpny_occurrences_with_forum_occurrences(company_occurrences :dict, forum_occ: int):
    multiplied_occurrences = {}
    for cpmny_name, occ_in_text in company_occurrences.items():
        multiplied_occurrences[cpmny_name] = occ_in_text * forum_occ
    return multiplied_occurrences


def calculate_occurrences_for_specific_date(date_str):
    folders_of_date = get_folders_of_date(date_str)
    json_manager = JsonManager()

    current = 1
    for folder in folders_of_date:
        # logger.info(f"processing_folder: {current}/{len(folders_of_date)}")
        # current += 1
        asses_download_batch(folder, json_manager)

    return json_manager


def asses_download_batch(download_folder, json_manager: JsonManager):
    global tickers

    downloaded_jsons = list_files(download_folder)
    result = {}
    current_num = 1
    for json_path in downloaded_jsons:
        # logger.info(f"\t processing data: {current_num}/{len(downloaded_jsons)}")
        # current_num += 1
        json_manager.add_json_path(json_path)
    return result


def calculate_match_report_for_file(json_path):
    text = open_file(json_path)
    cmpny_name_matches = search_for_company_names(text)
    symbol_matches = search_for_tickers(text)
    match_report = MatchReport(json_path, cmpny_name_matches, symbol_matches)
    return match_report


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

# print(search_for_expression(""" Nvidia shareholders giving away sh""", "Nvidia"))
