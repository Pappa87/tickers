import datetime

import config
from typing import Dict, List
from datetime import date
import requests
import json
from portfolio_tester.portfolio_tester_commons import *

class OpenCloseValue:
    def __init__(self, open, close):
        self.open = open
        self.close = close

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Open: {self.open}, Close: {self.close}"


class CompanyHistoricalData:

    def __init__(self, symbol):
        self.symbol = symbol
        self.data: Dict[date, OpenCloseValue] = {}

    def add_data(self, date_time, open, close):
        self.data[date_time] = OpenCloseValue(open, close)

    def get_data(self, date_time):
        if date_time in self.data.keys():
            return self.data[date_time]
        else:
            self.add_historical_data()
            return self.data[date_time]


    def add_historical_data(self):
        url =f'https://financialmodelingprep.com/api/v3/historical-price-full/{self.symbol}?apikey={config.TICKER_API_KEY}'
        result = requests.get(url).text
        json_result = json.loads(result)

        for data in json_result["historical"]:
            date = string_to_date(data["date"])
            open = data["open"]
            close = data["close"]
            self.add_data(date, open, close)
        return


class HistoricalStockManager:

    def __init__(self):
        self.data : Dict[str, CompanyHistoricalData] = {}

    def get_historical_data(self, symbol, date_time):
        try:
            if symbol in self.data.keys():
                return self.data[symbol].get_data(date_time)
            else:
                self.data[symbol] = CompanyHistoricalData(symbol)
                return self.data[symbol].get_data(date_time)
        except Exception as e:
            raise Exception("no data found for given day")

    def get_growth_of_symbol(self, symbol, from_date, to_date):
        begin_open = self.get_historical_data(symbol, from_date).open
        end_open = self.get_historical_data(symbol, to_date).open
        growth = end_open / begin_open
        return growth

    def get_market_days(self):
        self.get_historical_data("AAPL", datetime.date(2025, 3, 18))
        market_days = list(self.data["AAPL"].data.keys())
        market_days.sort()
        return market_days