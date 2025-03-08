from request_ticker_counter.ticker_counter_commons import *

def log_matches(match_report: MatchReport, result):
    if len(match_report.cmpny_name_matches) != 0 or len(match_report.symbol_matches) != 0:
        logger.info(f'analyzing: {match_report.json_name}')
        if len(match_report.cmpny_name_matches) != 0:
            logger.info(f"cmpny_name_matches: {match_report.cmpny_name_matches}")
        if len(match_report.symbol_matches) != 0:
            logger.info(f"symbol_matchess: {match_report.symbol_matches}")
        logger.info("")
        logger.info(f"CURRENT: {result}")
        logger.info("")


def log_matches_text_environment(path_to_text, matches, tickers):
    unique_matches = list(set(matches))
    for company_name in unique_matches:

        simplified_ticker = simplify_ticker_name(company_name)
        matches = text_environment(file_path=path_to_text, search_word=simplified_ticker)
        if len(matches) > 0:
            logger.info(f"MATCHES in company names: {company_name}")
            for match in matches:
                logger.info(f"\t {str.strip(match[:-1])}")


        symbol = get_symbol(company_name, tickers)
        matches = text_environment(file_path=path_to_text, search_word=symbol)
        if len(matches) > 0:
            logger.info(f"MATCHES in symbol: {company_name}")
            for match in matches:
                logger.info(f"\t {str.strip(match[:-1])}")


def get_symbol(cmpny_name, tickers):
    for ticker in tickers:
        if ticker.name == cmpny_name:
            return ticker.symbol
    return None
