# src/IRS/wrappers.py

import pandas as pd

from .smb_retrievals import get_irs_df
from .calc import irs_interpolate, discount_factor, zero_rates, forward_rates


def calculate_irs(irs_df: pd.DataFrame,
                  term: int = 0.25) -> pd.DataFrame:
    """
    Receives IRS dataframe and interpolates into designated terms.

    Then after, add discount factors, zero rates and forward rates
    """
    irs = irs_df["irs"].values.tolist()
    m = irs_df["기일물"].values.tolist()

    irs, m = irs_interpolate(term, irs, m)

    d = discount_factor(irs, m)
    z = zero_rates(d, m)
    f = forward_rates(d, m)

    df = pd.DataFrame({
        "maturity": m,
        "irs": irs,
        "discount_factor": d,
        "zero_rates": z,
        "forward_rates": f
    })
    return df


def get_irs(
    date: str,
    cd_rate: float) -> pd.DataFrame:
    """
    Gets IRS dataframe from the SMB Website
    Needs to specify cd_rates for the day since the website does not offer
    data on cd_rates
    """
    df = get_irs_df(date, cd_rate)
    df = calculate_irs(df)

    return df
