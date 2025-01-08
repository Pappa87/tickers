import json
import requests

def get_tickers():
    url = "https://financialmodelingprep.com/api/v3/stock/list"
    api_keys = json.load(open("C:\\tmp\\ticker_test_data\\api_keys.json", "r"))
    financialmodelingprep_api_key = api_keys["financialmodelingprep"]

    response = requests.get(f"{url}?apikey={financialmodelingprep_api_key}")

    if response.status_code == 200:
        stocks = response.json()
        print("Number of stocks:", len(stocks))
        ticker_list = []
        for stock in stocks:
            if (
                    ("." not in stock["symbol"])
                        &
                    (len(stock["symbol"]) > 2)
                        &
                    (stock["exchange"] == "NASDAQ")
            ):
                ticker_list.append(stock["symbol"])
        return ticker_list


    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")