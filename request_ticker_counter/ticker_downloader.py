import json
import requests

import config


class Stock:

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return f"Stock: ({self.name}: {self.symbol})"

    def __repr__(self):
        return self.__str__()

def get_tickers():
    url = "https://financialmodelingprep.com/stable/sp500-constituent"
    financialmodelingprep_api_key = config.TICKER_API_KEY

    response = requests.get(f"{url}?apikey={financialmodelingprep_api_key}")

    if response.status_code == 200:
        stocks = response.json()
        print("Number of stocks:", len(stocks))
        ticker_list = []
        for stock in stocks:
            ticker_list.append(Stock(stock["name"], stock["symbol"]))
        return ticker_list


    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")