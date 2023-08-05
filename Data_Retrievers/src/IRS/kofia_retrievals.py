# src/IRS/smb_retrievals.py

# import native python modules
import asyncio

# import 3rd party packages
from pyppeteer import launch
from bs4 import BeautifulSoup
from bs4.element import Tag

# import pandas
import pandas as pd


def _extract_irs_table(
        irs_table: Tag,
        cd_rate: float) -> pd.DataFrame:
    """
    Internal function which receives two arguments and returns a dataframe of IRS Table
    1) irs_table arg is supposed to be a 'find_all' [0] return from the raw html of SMB website
    this function will extract tenor and irs data from the html.
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-using-tag-names

    2) CD_rates are not retrievable from the webpage which the irs rates are extracted, thus it will
    receive CD_rates manually to complete the IRS table
    """
    data_list = list({"3M": cd_rate})
    for tr in irs_table.find_all("tr"):
        # get all table rows and initialize and append it in the list
        data = dict()
        for th, td in zip(irs_table.select('th'), tr.select("td")):
            # match each tr data with column heads
            data[th.text.strip()] = td.text.strip()
            data_list.append(data)

    # set them as df and drop duplicate rows
    df = pd.DataFrame(data_list)
    df = df.drop_duplicates()
    return df


async def _get_irs_html(
        date: str):
    """
    This asynchronous function retrieves IRS html from the SM website
    It receives the 'date' string argument which serves as the website "조회하기" input
    'date' must be 6 characters long, for example: "20200404"
    """
    # start a headless browser to retrieve raw html from the SMB website
    browser = await launch(headless=False, autoClose=False)
    page = await browser.newPage()
    await page.goto('http://www.smbs.biz/Exchange/IRS.jsp')
    await page.waitFor(2000)

    # click on the searchDate Input Field to activate javascript
    elements = await page.xpath("//input[contains(@id, 'searchDate')]")
    await elements[0].click()
    await page.waitFor(1000)

    # change the searchdate through javascript
    await page.evaluate(f"""() => {{
        document.getElementById('searchDate').value = '{date}';
    }}""")

    # click on 조회하기
    elements = await page.xpath("//img[contains(@alt, '조회하기')]")
    await elements[0].click()

    # get html content
    html = await page.content()
    await browser.close()
    return html


def get_irs_df(
        date: str,
        cd_rate: float) -> pd.DataFrame:
    """
    This function receives 2 arguments: 'date' and 'CD_rate'.
    1) It receives the 'date' string argument which serves as the website "조회하기" input
    'date' must be 6 characters long, for example: "20200404"
    2) Since the SMB website does not serve CD_rate data, and to successfully calculate
    discount factors and forward rates from IRS data, CD_rates(risk free) are necessary.
    CD_rates must be given by float types
    """
    html_response = asyncio.get_event_loop().run_until_complete(_get_irs_html(date))
    # Load HTML Response Into BeautifulSoup
    soup = BeautifulSoup(html_response, "html.parser")

    # isolate irs table from other data
    irs_table = soup.find_all("div", attrs={"class": "table_type2"})[0]

    # get date data
    date = soup.find_all("input", attrs={"name": "StrSchFull3"})[0]
    print(f"date = {date.text.strip()}")

    df = _extract_irs_table(irs_table, cd_rate)
    return df
