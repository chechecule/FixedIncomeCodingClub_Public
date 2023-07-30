# src/IRS/archived_for_later.py

"""
This file was specifically created to store rate calculators which keonsun has written
on his attempt to write calculating codes for IRS.
The codes here are meant to work from Treasury Bonds, and not for IRS
"""


def _get_spot(i, spot_rates, par_rates, maturity):
    """

    """
    # get discount_val except final tenor
    discount_mat = 0
    for n in range(i):
        discount_mat += (par_rates[i] * 100) / ((1 + spot_rates[n]) ** (maturity[n]))

    spot_i = (((100 + (par_rates[i] * 100)) / (100 - discount_mat)) ** (1 / maturity[i])) - 1

    return spot_i

def _get_forward(spot_rates, maturity):
    forward_rates = list()
    forward_rates.append(spot_rates[0])

    for i in range(1, len(spot_rates)):
        mat_diff = maturity[i] - maturity[i - 1]

        forward_rate = (1 + spot_rates[i]) ** maturity[i] / ((1 + spot_rates[i - 1]) ** maturity[i - 1]) - 1
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