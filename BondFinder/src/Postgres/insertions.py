# PG/insertions.py

import psycopg2
import psycopg2.extras
import pandas as pd


def insert_to_db(conn, table_name, df, **kwargs):
    cur = conn.cursor()

    insert_string = \
    f"""INSERT INTO {table_name} {"(" + ", ".join(df.columns.to_list()) + ")"} VALUES %s """

    # set kwargs
    if kwargs.get('ignore_duplicates', True):
        insert_string += f"ON CONFLICT ON CONSTRAINT {table_name}_key DO NOTHING;"

    else:
        do_string = \
        f"""ON CONFLICT ON CONSTRAINT {table_name}_key DO UPDATE SET {
            ", ".join(
            [str(col) + " = excluded." + str(col) for col in df.columns.to_list()]
            )
        };"""

    psycopg2.extras.execute_values(
        conn.cursor(),
        insert_string,
        tuple(df.to_numpy())
    )
    conn.commit()
