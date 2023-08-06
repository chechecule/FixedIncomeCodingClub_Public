# PG/retrievals.py

import psycopg2
import pandas as pd

def psql_to_pd(conn, sql_string, **kwargs):
    cur = conn.cursor()

    cur.execute(sql_string)
    data = cur.fetchall()
    cols = list(map(lambda x: x[0], cur.description))

    return pd.DataFrame(data, columns=cols)
