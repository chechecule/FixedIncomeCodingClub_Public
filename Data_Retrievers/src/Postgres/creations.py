# PG/creations.py

import psycopg2

def create_database_tables(conn, creation_dict, table_names):
    for table_name in table_names:
        creation_string = creation_dict.get(table_name, False)
        if creation_string:
            create_database_table(conn, creation_string)
        else:
            print(f"table {creation_string} does not exist in creation_dict")


def create_database_table(conn, creation_string):
    cur = conn.cursor()
    if isinstance(creation_string, list):
        try:
            for creation in creation_string:
                cur.execute(creation)
        except Exception as e:
            print(e)
            print("rollback now")
            cur.execute("rollback;")
    elif isinstance(creation_string, str):
        try:
            cur.execute(creation_string)
        except Exception as e:
            print(e)
            print("rollback now")
            cur.execute("rollback;")
    else:
        raise RuntimeError(f"database creation string should be list or string. Current type is {type(creation_string)}")

    conn.commit()
