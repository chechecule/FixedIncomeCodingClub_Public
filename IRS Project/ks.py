import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

from collections import OrderedDict
from pprint import pprint

import pandas as pd

def _get_IRS_table(irs_table) -> pd.DataFrame:
    """
    IRS Table getter. this returns a df
    """

    data_list = list()

    for tr in irs_table.find_all("tr"):
        #get all table rows and initialize an ordered dict to ensure sequence
        data = OrderedDict()

        for th, td in zip(irs_table.select('th'), tr.select("td")):
            # match each tr data with column heads
            data[th.text.strip()] = td.text.strip()
            data_list.append(data)

    # set them as df and drop duplicate rows
    df = pd.DataFrame(data_list)
    df = df.drop_duplicates()
    #pprint(df)

    return df



async def main():
    browser = await launch(headless=False, autoClose=False)
    page = await browser.newPage()
    await page.goto('http://www.smbs.biz/Exchange/IRS.jsp')

    await page.waitFor(2000)

    await page.evaluate(f"""() => {{
        document.getElementById('searchDate').value = '';
    }}""")

    elements = await page.xpath("//input[contains(@id, 'searchDate')]")
    await elements[0].click()

    await page.waitFor(1000)
    target_date = "20230609"
    await page.type("#searchDate", target_date) 

    await page.waitFor(1000)
    elements = await page.xpath("//img[contains(@alt, '조회하기')]")
    await elements[0].click()


    html = await page.content()

    # await browser.close()
    return html

html_response = asyncio.get_event_loop().run_until_complete(main())

## Load HTML Response Into BeautifulSoup
soup = BeautifulSoup(html_response, "html.parser")

# isolate irs table from other data
irs_table = soup.find_all("div", attrs={"class" : "table_type2"})[0]

# get date data
date = soup.find_all("input", attrs={"name" : "StrSchFull3"})[0]
print(f"date = {date.text.strip()}")

df = _get_IRS_table(irs_table)
pprint(df)




