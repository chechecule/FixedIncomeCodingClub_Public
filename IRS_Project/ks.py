import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

from collections import OrderedDict, Sequence

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


def _get_spot(i, spot_rates, par_rates, maturity):
    """

    """

    # get discount_val except final tenor

    discount_mat = 0
    for n in range(i):
        discount_mat += (par_rates[i]*100)/((1+spot_rates[n])**(maturity[n]))

    spot_i = (((100+(par_rates[i]*100)) / (100-discount_mat))**(1/maturity[i])) - 1 

    return spot_i

def _get_forward(spot_rates, maturity):
    forward_rates = list()
    forward_rates.append(spot_rates[0])

    for i in range(1, len(spot_rates)):
        mat_diff = maturity[i] - maturity[i-1]
        
        forward_rate = (1+spot_rates[i])**maturity[i]/((1+spot_rates[i-1])**maturity[i-1])-1
        forward_rates.append(forward_rate)
    return forward_rates

def par_to_spot(
    par_rates : Sequence, 
    maturity : Sequence, 
    *args, **kwargs
    ) -> Sequence:

    # first check if length equals 
    assert len(par_rates) == len(maturity)

    spot_rates = list()
    spot_rates.append(par_rates[0])

    for i in range(1, len(par_rates)):
        spot_rates.append(
            _get_spot(i, spot_rates, par_rates, maturity)
        )

    return spot_rates

def spot_to_forward(
        spot_rates: Sequence,
        maturity: Sequence,
        *args, **kwargs
    ) -> Sequence:
    
    assert len(spot_rates) == len(maturity)

    return _get_forward(spot_rates, maturity)
        

def IRS_interpolate(term, irs, m, *args, **kwargs):

    interpolated_maturity = list()
    interpolated_irs_rates = list()


    for i in range(len(m)):
        if ((m[i] - m[i-1]) == term):
            interpolated_maturity.append(m(i))
            interpolated_irs_rates.append(irs(i))

        else:
            for inter_term in range(term, m[i-1], m[i]):
                interpolated_maturity.append(inter_term)
                interpolated_irs_rates.append(
                    irs[i] + \
                    (irs[i]-irs[i-1])/((inter_term-m[i])/(m[i]-m[i-1]))
                )

    return interpolated_irs_rates, interpolated_maturity

def discount_factor(irs, m):
    discount = list()
    discount.append(
        1/(1+irs[0]/((1/m[1]-m[0])))
        )
    """
    next one:
    (1-irs[1]/(1/m_diff)*discount[0])/(1+irs[1]/(1/m_diff))

    next one
    (1-irs[2]/(1/m_diff)*discount[0]-irs[2]/(1/m_diff)*discount[1])/(1+irs[2]/(1/m_diff))
    equals
    (1-irs[2]/(1/m_diff)*(discount[0]+discount[1]))/(1+irs[2]/(1/m_diff))
    """

    for i in range(1, len(m)):
        m_diff = m[i] - m[i-1]

        dis_i = (1-irs[i]/(1/m_diff)*sum(discount[:i-1]))\
        /(1+irs[i]/(1/m_diff))


        discount.append(dis_i)

    return discount

def spot_rates(irs_rates, discount_factors, maturity):

    spot_rates = list()

    spot_rates.append(
        irs_rates[0]
    )

    for i in range(1, len(irs_rates)):
        mat_diff = maturity[i] - maturity[i-1]
        spot_rates.append(
            ((1/discount_factors[i])**(1/(maturity[i]*(1/mat_diff)))-1)*(1/mat_diff)
            )


