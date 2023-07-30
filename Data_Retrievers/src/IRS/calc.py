# src/IRS/calc.py

# import native
import math
from collections.abc import Sequence


def irs_interpolate(
    term: float,
    irs: Sequence,
    m: Sequence) -> tuple[Sequence, Sequence]:

    interpolated_maturity = list()
    interpolated_irs_rates = list()

    for i in range(len(m)):
        if (m[i] - m[i-1]) == term:
            interpolated_maturity.append([i])
            interpolated_irs_rates.append(irs[i])
        else:
            for inter_term in range(m[i-1], m[i], term):
                interpolated_maturity.append(inter_term)
                interpolated_irs_rates.append(
                    irs[i] +
                    (irs[i]-irs[i-1]) /
                    ((inter_term-m[i])/(m[i]-m[i-1]))
                )
    return interpolated_irs_rates, interpolated_maturity


def discount_factor(
    irs: Sequence,
    m: Sequence) -> Sequence:

    discount = list()
    discount.append(
        1/(1+irs[0]/(1/m[1]-m[0]))
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
        dis_i = ((1-irs[i]/(1/m_diff)*sum(discount[:i-1])) /
                 (1+irs[i]/(1/m_diff)))
        discount.append(dis_i)

    return discount


def zero_rates(
    d: Sequence,
    m: Sequence) -> Sequence:
    """
    Zero 구하기
    df.loc['0.25','Zero'] = -math.log(df.loc['0.25','DF'])/0.25*100
    df.loc['0.50','Zero'] = -math.log(df.loc['0.50','DF'])/0.50*100
    df.loc['0.75','Zero'] = -math.log(df.loc['0.75','DF'])/0.75*100
    """
    z_rates = list()
    for i in range(0, len(d)-1):
        z_rates.append(
            -math.log(d[i])/m[i]
        )
    z_rates.append("None")
    return z_rates


def forward_rates(
    d: Sequence,
    m: Sequence) -> Sequence:
    """
    #forward
    df.loc['0.25','Forward']=(df.loc['0.25','DF'] / df.loc['0.50','DF']-1)/(0.25)*100
    df.loc['0.50','Forward']=(df.loc['0.50','DF'] / df.loc['0.75','DF']-1)/(0.25)*100
    df.loc['0.75','Forward']=(df.loc['0.75','DF'] / df.loc['1.00','DF']-1)/(0.25)*100
    """
    f_rates = list()
    for i in range(0, len(d)-1):
        f_rates.append(
            (d[i]/d[i+1]-1)/m[i]
        )
    return f_rates
