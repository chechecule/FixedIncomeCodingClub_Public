# pandas_function.py

# import re
import re

# import third party library
import pandas as pd

# set re
only_strings = re.compile("[^0-9]")

def df_datestring_to_datetime(df):
    '''
    Changes the dataframe's date string YYYYMMDD format to datetime object.
    '''
    df['date'] = df['date'].apply(
        lambda x: pd.to_datetime(str(x), format='%Y%m%d').strftime('%Y-%m-%d')
    )
    return df

def df_code_strip_noninteger(df):
    '''
    Strips non integer from the dataframe's code column.
    Ex) A000020 -> 000020
    '''
    df['code'] = df['code'].apply(
        lambda x: only_strings.sub(r'', x)
    )
    return df
