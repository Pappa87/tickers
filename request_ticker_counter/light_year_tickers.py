import requests
from typing import List
from bs4 import BeautifulSoup, Tag
from json_parse_approach.common import logger
import time
import config
import google.generativeai as genai
import ast

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')


class CompanyData:

    def __init__(self, company_name, ticker, searchable_expressions):
        self.company_name = company_name
        self.ticker = ticker
        self.searchable_expressions: List[str] = searchable_expressions

    def make_it_csv_line(self):
        return f"{self.company_name};{self.ticker};{self.searchable_expressions}\n"

    def add_searchable_expressions(self, searchable_expressions):
        if searchable_expressions is not None:
            self.searchable_expressions.extend(searchable_expressions)

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
        csv_test += company_data.make_it_csv_line()
    return csv_test


def add_alternative_company_names_to_company_list(company_list: List[CompanyData]):
    index = 0
    for company_data in company_list:
        index += 1
        logger.info(f"{index}/{len(company_list)}")
        add_alternative_company_names(company_data)


def add_alternative_company_names(company_data: CompanyData):
    global model
    company_name = company_data.company_name
    question = (f"is there simple alternative way people refer to {company_name} (company), "
                f'if yes return them in the following format: ["alternative1", "alternative2"....], '
                f"if there is no good answer please return with None")
    response = model.generate_content(question)
    parsed_response = parse_gemini_response(response.text)
    company_data.add_searchable_expressions(parsed_response)


def parse_gemini_response(response):
    lines = response.split("\n")
    answer = lines[1]
    try:
        if answer == "None":
            return None
        else:
            return ast.literal_eval(answer)
    except Exception as e:
        logger.error("error while parsing alternatives")
        logger.error(f"response to parse: \n")
        logger.error(response)
        return ["ERROR"]


def main():
    company_datas = collect_company_data(); company_datas = company_datas[0:3]
    add_alternative_company_names_to_company_list(company_datas)
    csv_data = create_csv_of_company_datas(company_datas)
    print(csv_data)
    print("DONE")




if __name__ == "__main__":
    main()