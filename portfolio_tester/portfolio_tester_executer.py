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
        strategy_days_set = set(self.portfolios.keys())

        market_days = self.historical_stock_manager.get_market_days()
        market_days_set = set(market_days)

        analyzed_days = list(strategy_days_set.intersection(market_days_set))
        analyzed_days.sort()

        last_day_of_strategy = analyzed_days[-1]
        next_day_of_market = market_days[market_days.index(last_day_of_strategy) + 1]
        analyzed_days.append(next_day_of_market)

        return analyzed_days

    def norm_growth(self):
        analyzed_days = self.get_analyzed_days()

        day_indexes = range(0, len(analyzed_days) -1)
        total_growth = 1
        for day_index in day_indexes:
            day = analyzed_days[day_index]
            following_market_day = analyzed_days[day_index + 1]
            norm_growth_of_date = self.get_norm_growth_of_date(day, following_market_day)
            total_growth *= norm_growth_of_date
        return total_growth

    def get_norm_growth_of_date(self, begin, end):
        portfolio = self.get_portfolio(begin)

        total_growth = 0
        for investment in portfolio.investments:
            growth = self.historical_stock_manager.get_growth_of_symbol(investment.symbol, begin, end)
            growth_of_company = (investment.volume) * growth
            total_growth = total_growth + growth_of_company

        total_value_of_investment = portfolio.get_total_value()
        normalized_growth = total_growth /total_value_of_investment
        return normalized_growth


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.portfolios)


# main.py
def main():
    day_1 = datetime.date(2025, 3, 11)
    day_2 = datetime.date(2025, 3, 12)
    day_3 = datetime.date(2025, 3, 13)

    strategy = Strategy()
    strategy.add_investment(day_1, "AAPL", 10)
    strategy.add_investment(day_2, "AAPL", 5)
    strategy.add_investment(day_3, "AAPL", 8)

    strategy.add_investment(day_1, "TSLA", 4)
    strategy.add_investment(day_2, "TSLA", 5)
    strategy.add_investment(day_3, "TSLA", 6)
    norm_growth = strategy.norm_growth()

    return

if __name__ == "__main__":
    main()