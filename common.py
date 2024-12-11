import time
import asyncio


async def get_article_hrefs(article_selector, page):
    article_elems = await page.querySelectorAll(article_selector)
    article_href_promises = [page.evaluate("(element) => element.getAttribute('href')", elem) for elem in article_elems]
    article_hrefs = await asyncio.gather(*article_href_promises)
    article_hrefs_filtered = [article for article in article_hrefs if article.startswith('/r/wallstreetbets/comments/')]
    return set(article_hrefs_filtered)

async def scroll_down(page, SCROLLING_NUM, WAIT_BETWEEN_SCROLLING):
    for current_scroll in range(0, SCROLLING_NUM):
        await page.evaluate("""{window.scrollBy(0, document.body.scrollHeight);}""")
        time.sleep(WAIT_BETWEEN_SCROLLING)


async def scroll_down_little(page, SCROLLING_NUM, WAIT_BETWEEN_SCROLLING):
    for current_scroll in range(0, SCROLLING_NUM):
        await page.evaluate("""{window.scrollBy(0, 10);}""")
        time.sleep(WAIT_BETWEEN_SCROLLING)

