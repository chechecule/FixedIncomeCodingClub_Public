
# import native python modules
import asyncio
import math
from collections.abc import Sequence

# import 3rd party packages
from pyppeteer import launch
from bs4 import BeautifulSoup
# import pandas
import pandas as pd

def _extract_irs_table(
        irs_table: Sequence,
        CD_rates: float
    ) -> pd.DataFrame:
    """
    Internal function which receives two arguments and returns a dataframe of IRS Table
    1) irs_table arg is supposed to be a 'find_all' return from the raw html of SMB website
    this function will extract tenor and irs data from the html.
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-using-tag-names

    2) CD_rates are not retrievable from the webpage which the irs rates are extracted, thus it will
    receive CD_rates manually to complete the IRS table
    """
    data_list = list({"3M" : CD_rates})
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
        date: str
    ):
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

    # click on the searcDate Input Field to activate javascript
    elements = await page.xpath("//input[contains(@id, 'searchDate')]")
    await elements[0].click()
    await page.waitFor(1000)

    # change the searchdate through javascript
    await page.evaluate(f"""() => {{
        document.getElementById('searchDate').value = '{date}';
    }}""")

    #click on 조회하기
    elements = await page.xpath("//img[contains(@alt, '조회하기')]")
    await elements[0].click()

    # get html content
    html = await page.content()
    await browser.close()
    return html

def get_irs_df(
        date: Str,
        CD_rate: float
    ) -> pd.DataFrame:
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

    df = _extract_irs_table(irs_table, CD_rate)
    return df

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
    par_rates: Sequence,
    maturity: Sequence,
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

def discount_factor(
        irs : Sequence,
        m : Sequence
    ) -> Sequence:
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

def zero_rates(
    d : Sequence, 
    m : Sequence
    ) -> Sequence:
    """
    Zero 구하기
    df.loc['0.25','Zero'] = -math.log(df.loc['0.25','DF'])/0.25*100
    df.loc['0.50','Zero'] = -math.log(df.loc['0.50','DF'])/0.50*100
    df.loc['0.75','Zero'] = -math.log(df.loc['0.75','DF'])/0.75*100
    """
    zero_rates = list()
    for i in range(0, len(d)-1):
        zero_rates.append(
            -math.log(d[i])/m[i]
        )
    zero_rates.append("None")
    return zero_rates


def forward_rates(
    d : Sequence,
    m : Sequence
    ) -> Sequence:
    """
    #forward
    df.loc['0.25','Forward']=(df.loc['0.25','DF'] / df.loc['0.50','DF']-1)/(0.25)*100
    df.loc['0.50','Forward']=(df.loc['0.50','DF'] / df.loc['0.75','DF']-1)/(0.25)*100
    df.loc['0.75','Forward']=(df.loc['0.75','DF'] / df.loc['1.00','DF']-1)/(0.25)*100
    """
    forward_rates = list()

    for i in range(0, len(d)-1):
        mat_dff = m[i+1] - m[i]
        forward_rates.append(
            (d[i]/d[i+1]-1)/m[i]
        )
    return forward_rates






