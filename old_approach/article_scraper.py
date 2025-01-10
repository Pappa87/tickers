from common import *

SCROLLING_NUM = 1
WAIT_BETWEEN_SCROLLING = 1


async def scrape_article(page, article_identifier):
    await go_to_article(page, article_identifier)
    return ''


async def go_to_article(page, article_identifier):
    url = f"https://www.reddit.com/{article_identifier}"
    await page.goto(url)
    for i in range(0,5):
        await scroll_down(page, SCROLLING_NUM, WAIT_BETWEEN_SCROLLING)


async def expand_forum(page):
    expand_buttons = await page.querySelectorAll('svg[icon-name="join-outline"]')
    for expand_button in expand_buttons:
        is_visible = await expand_button.isIntersectingViewport()
        if is_visible:
            await page.evaluate('(el) => el.scrollIntoView()', expand_button)  # Scroll into view
            await expand_button.click()
            print('valid expanding')
        else:
            print("Element not visible, skipping.")