import main_page_scraper
import article_scraper
import asyncio
from pyppeteer import launch

async def main():

    browser = await launch(
        headless=False,
        args=['--no-sandbox', '--disable-setuid-sandbox'],
        executablePath="C:\Program Files\Google\Chrome\Application\chrome.exe"
    )
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 2000})

    # articles = await main_page_scraper.get_articles(page, "wallstreetbets")
    # print(articles)

    scraped_article = await article_scraper.scrape_article(page, 'r/wallstreetbets/comments/1h7kn77/80k_to_888k_in_about_15_years_leveraging_with/')


    # await browser.close()



asyncio.get_event_loop().run_until_complete(main())