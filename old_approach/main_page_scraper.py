from common import *

SCROLLING_NUM = 1
WAIT_BETWEEN_SCROLLING = 2
ARTICLE_NUM_TRSH = 50


async def get_articles(page, subreddit):
    await go_to_subreddit(page, subreddit)

    article_hrefs = set()
    while len(article_hrefs) < ARTICLE_NUM_TRSH:
        await scroll_down(page, SCROLLING_NUM, WAIT_BETWEEN_SCROLLING)
        article_hrefs = await get_article_hrefs("article a", page)
    return article_hrefs


async def go_to_subreddit(page, subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/new/"
    await page.goto(url)





