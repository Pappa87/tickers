import requests
import time
import config

def parse_article_list(subreddit_id, order = "hot"):
    time.sleep(config.WAIT)
    url = f"https://www.reddit.com/r/{subreddit_id}/{order}.json?limit=100"

    response = requests.get(url,
            headers={'User-agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    json_response = response.json()
    articles_raw = json_response["data"]["children"]
    article_links = []
    for article in articles_raw:
        article_links.append(article["data"]["permalink"])

    return article_links




