import psycopg2


def connect_to_db(**kwargs):

    """
    Connect cursor to postgresql database
    """
    conn = psycopg2.connect(
        f'''host={kwargs.get('host')}
        dbname={kwargs.get('dbname')}
        user={kwargs.get('user')}
        port={kwargs.get('port')}
        password={kwargs.get('password')}
        '''
        )
    return conn
