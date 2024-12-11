import asyncio
from pyppeteer import launch

proxy = True
headless = True

def conf_browser(headless_ = True, proxy_ = False):
    global proxy
    global headless
    headless = headless_
    proxy = proxy_

async def get_browser():
    params = set_up_params()
    browser = await launch(
        params
    )
    return browser


def set_up_params():
    global proxy
    global headless

    args = []
    if proxy:
        args.append('--proxy-server=eu.lumiproxy.com:5888')

    params = {
        "headless": headless,
        "args": args
    }

    return params


async def close_browser(browser):
    await browser.close()


async def get_page(browser):
    page = await browser.newPage()
    if(proxy):
        await page.authenticate({
            'username': 'lumi-pappaScraper',
            'password': 'Scraper87'
        })
    await make_it_stealth(page)
    #await page.setJavaScriptEnabled(True)
    #await not_load_waste(page)
    return page


async def intercept(request):
    print(request.resourceType)
    # if request.url.endswith('.png') or request.url.endswith('.jpg'):
    if request.resourceType == 'image':
        await request.abort()
    else:
        await request.continue_()


async def not_load_waste(page):
    await page.setRequestInterception(True)
    page.on('request', lambda req: asyncio.ensure_future(intercept(req)))


async def make_it_stealth(page):
    # USER AGENT TEST
    userAgent = 'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.39 Safari/537.36'
    await page.setUserAgent(userAgent)


async def get_text(element):
    prop = await element.getProperty('innerText')
    value = await prop.jsonValue()
    return value


async def get_ip(browser):
    page = await get_page(browser)
    await page.goto('https://api.ipify.org/')
    body = await page.querySelector('body')
    ip = await get_text(body)
    print(f"ip: {ip}")
    await page.close()

