import logging
import time

import requests
from article import Article, Comment
import config
import os
from common import logger

def parse_article(article_identifier, time_stamp):
    time.sleep(config.WAIT)
    url = f"https://www.reddit.com{article_identifier}.json"
    logging.info(f"url: {url}")

    response = requests.get(url, headers = {'User-agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    logger.info(f"response code:{response.status_code}")
    json_response = response.json()
    logger.info(f"response sample: {str(json_response)[0:200]}")

    article_data_raw = json_response[0]["data"]["children"][0]["data"]
    root_comments_raw = json_response[1]["data"]["children"]

    article_parsed = Article.parse_article(article_data_raw)
    comments_parsed = Comment.parse_comments(root_comments_raw)
    article_parsed.add_comments(comments_parsed)

    write_article_file(article_parsed, article_identifier, time_stamp)


def write_article_file(article, article_id, time_stamp):
    logger.info("writing to file")
    file_name = create_file_name(article_id, time_stamp)
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(article.to_json())

    logger.info("file writing succesfull")
    logger.info(f"filename: {file_name}")


def create_file_name(article_id, time_stamp):

    check_and_create_todays_directory(time_stamp)

    file_name = f"""{config.SAVING_FOLDER}/{time_stamp}/{article_id.replace("/", "__")}__{time_stamp}.json"""
    return file_name


def check_and_create_todays_directory(today_string):
    directory_path = f"{config.SAVING_FOLDER}/{today_string}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

