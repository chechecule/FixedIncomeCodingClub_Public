# src/IRS/wrappers.py

import pandas as pd

from .smb_retrievals import get_irs_df
from .calc import irs_interpolate, discount_factor, zero_rates, forward_rates


def calculate_irs(
    irs_df: pd.DataFrame) -> pd.DataFrame:
    irs = irs_df["irs"].values.tolist()
    m = irs_df["기일물"].values.tolist()

    irs, m = irs_interpolate(0.25, irs, m)

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
    df = get_irs_df(date, cd_rate)
    df = calculate_irs(df)

    return df


