from datetime import timedelta
from portfolio_tester.historical_stock_manager import *


class Investment:
    def __init__(self, symbol, volume):
        self.symbol = symbol
        self.volume = volume

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.symbol} : {self.volume}"


class Portfolio:

    def __init__(self):
        self.investments: List[Investment] = []

    def add_symbol(self, symbol, volume):
        investment = Investment(symbol, volume)
        self.investments.append(investment)

    def get_total_value(self):
        sum = 0
        for investment in self.investments:
            sum += investment.volume
        return sum


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.investments)


class Strategy:

    def __init__(self):
        self.portfolios: Dict[datetime.date, Portfolio] = {}
        self.historical_stock_manager = HistoricalStockManager()

    def get_portfolio(self, date_time):
        return self.portfolios[date_time]

    def add_investment(self, date_time, symbol, volume):
        if date_time not in self.portfolios.keys():
            portfolio = Portfolio()
            portfolio.add_symbol(symbol, volume)
            self.portfolios[date_time] = portfolio
        else:
            self.get_portfolio(date_time).add_symbol(symbol, volume)


    def get_analyzed_days(self):
        strategy_days = set(self.portfolios.keys())
        market_days = set(self.historical_stock_manager.get_market_days())
        analyzed_days = list(strategy_days.intersection(market_days))
        analyzed_days.sort()
        return analyzed_days

    def homo_growth(self):
        analyzed_days = self.get_analyzed_days()
        for days in range(0, len(analyzed_days)):
            self.homo_growth_of_date(be)
        return

    def homo_growth_of_date(self, begin, end):
        portfolio = self.get_portfolio(begin)
        total_value_of_investment = portfolio.get_total_value()

        total_growth = 1
        for investment in portfolio.investments:
            growth = self.historical_stock_manager.get_growth_of_symbol(investment.symbol, begin, end)
            homo_growth = (investment.volume / total_value_of_investment) * growth
            total_growth = total_growth * homo_growth
        return total_growth


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.portfolios)


# main.py
def main():
#     day_1 = datetime.date(2025, 3, 11)
#     day_2 = datetime.date(2025, 3, 12)
#     day_3 = datetime.date(2025, 3, 13)
#
#     strategy = Strategy()
#     strategy.add_investment(day_1, "AAPL", 10)
#     strategy.add_investment(day_2, "AAPL", 5)
#     strategy.add_investment(day_3, "AAPL", 8)
#
#     strategy.add_investment(day_1, "TSLA", 4)
#     strategy.add_investment(day_2, "TSLA", 5)
#     strategy.add_investment(day_3, "TSLA", 6)
#     strategy.homo_growth()

    strategy = Strategy()
    for i in range(1, 29):
        strategy.add_investment(datetime.date(2025, 2, i), "AAPL", 10)
    strategy.homo_growth()
    return

if __name__ == "__main__":
    main()