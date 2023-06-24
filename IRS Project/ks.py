import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

import pandas as pd

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://www.smbs.biz/Exchange/IRS.jsp')

    ## Get Title
    ## Get HTML
    html = await page.content()
    await browser.close()
    return html

html_response = asyncio.get_event_loop().run_until_complete(main())

## Load HTML Response Into BeautifulSoup
soup = BeautifulSoup(html_response, "html.parser")
title = soup.find('h1').text
print('title', title)

df_list = pd.read_html(html_response)

print(df_list)

