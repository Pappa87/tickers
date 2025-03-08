import json
import requests

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
    api_keys = json.load(open("C:\\tmp\\ticker_test_data\\api_keys.json", "r"))
    financialmodelingprep_api_key = api_keys["financialmodelingprep"]

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