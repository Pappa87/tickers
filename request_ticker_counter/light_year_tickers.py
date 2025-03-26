import requests
from typing import List
from bs4 import BeautifulSoup, Tag
from json_parse_approach.common import logger
import time
import config

class CompanyData:

    def __init__(self, company_name, ticker, searchable_expressions):
        self.company_name = company_name
        self.ticker = ticker
        self.searchable_expressions = searchable_expressions

    def make_it_csv_line_without_expr(self):
        return f"{self.company_name};{self.ticker}\n"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.company_name} : {self.ticker} : {self.searchable_expressions}"


def get_company_data_from_company_elem(company_elem: Tag) -> CompanyData:
    company_name = company_elem.find("h2").text
    ticker = company_elem.find("div", attrs={"class": "text-body-small-bold"}).text.split("·")[0][1:]
    searchable_expressions = []
    return CompanyData(company_name, ticker, searchable_expressions)


def get_company_elems(html_content) -> Tag:
    soup = BeautifulSoup(html_content, "html.parser")
    company_elems = soup.find_all("div", attrs={"class": "sc-c45d095c-0 jYBKTa"})
    return company_elems


def get_html_content(page_index):
    result = requests.get(f"https://lightyear.com/en/stocks/explore?page={page_index}")
    time.sleep(2)
    html_content = result.content
    return html_content

def get_company_data_of_page(page_index):
    html_content = get_html_content(page_index)
    company_elems = get_company_elems(html_content)

    company_datas: List[CompanyData] = []
    for company_elem in company_elems:
        company_data = get_company_data_from_company_elem(company_elem)
        company_datas.append(company_data)

    return company_datas


def collect_company_data() -> List[CompanyData]:
    NUMBER_OF_PAGES = 2
    indexes = range(1, NUMBER_OF_PAGES + 1)
    company_data = []
    for index in indexes:
        logger.info(f"ticker downloader progress: {index}/{len(indexes)}")
        sub_company_data = get_company_data_of_page(index)
        company_data.extend(sub_company_data)
    return company_data


def create_csv_of_company_datas(company_datas: List[CompanyData]):
    csv_test = ""
    for company_data in company_datas:
        csv_test += company_data.make_it_csv_line_without_expr()
    return csv_test


import google.generativeai as genai


def main():
    company_datas = collect_company_data()

    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    for company_data in company_datas:
        company_name = company_data.company_name
        print(f"company_name: {company_name}")

        question = (f"I want to search for the following company: {company_name}, in a reddit forum, can you give me alternatives, that can refer to it by reddit users.\n"
                    f"if you cant come up any good alternative answer None.\n"
                    f"Use the following format in the response: [alternative1, alternative2....]. No other text required.")
        response = model.generate_content(question)
        print(question)
        print("alternatives: ")
        print(response.text)
        time.sleep(10)

if __name__ == "__main__":
    main()