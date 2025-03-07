from datetime import datetime
from common import logger
from article_list_parser import parse_article_list
from article_parser import parse_article
import config
import time
import schedule


def download(subreddit):
    today_string = datetime.today().strftime('%Y_%m_%d__%H_%M_%S')

    logger.info(f"start to scrape reddit {subreddit} for hot 100")
    comment_wall_links = parse_article_list(subreddit, order="hot")
    logger.info(f"found {len(comment_wall_links)} number of comment walls")
    logger.info(f"found comment walls: {comment_wall_links}")
    logger.info("")

    parsed_count = 0
    for link in comment_wall_links:
        logger.info(f"scraping the following comment wall: {link}")
        try_to_run_parser(link, today_string)
        parsed_count += 1
        logger.info(f"Successfully parsed {parsed_count}/{len(comment_wall_links)} comment walls")
        logger.info("")


def try_to_run_parser(link, today_string):
    max_retries = 3
    attempts = 0

    while attempts < max_retries:
        try:
            parse_article(link, today_string)
            return
        except Exception as e:
            attempts += 1
            logger.error(f"Attempt {attempts} failed: {e}")
            logger.error(f"An error occurred: {e} (Error type: {type(e).__name__})")
            if attempts < max_retries:
                logger.error(f"Retrying... ({attempts}/{max_retries})")
                time.sleep(config.WAIT)
            else:
                logger.error(f"Max retries reached. Skipping.")
                return


def job_to_run():
    download("wallstreetbets")

print("reddit scraper started: \n")
# make it run without scheduling first:)
job_to_run()
# Schedule the task
schedule.every(5).minutes.do(job_to_run)
while True:
    schedule.run_pending()
    time.sleep(1)