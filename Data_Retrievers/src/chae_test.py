from API.FSC import wrappers

#wrappers를 가져옴.

a = wrappers.getBondData(basDt="20230803")
#데이터 가져오기

a.columns
print(a)
a[["basDt", "scrsItmsKcdNm", "bondIsurNm", "bondSrfcInrt"]]

'''
import psycopg2

from utils import env_functions

from Postgres.connect import connect_to_db
from Postgres.creations import create_database_table
from Postgres.insertions import insert_to_db
from Postgres.retrievals import psql_to_pd

env_functions.get_dotenv("aws_pg_env.env")


conn = connect_to_db(
    host = "localhost",
    port = "5432",
    user = "keonsunkim",
    password = "04200812Rjs!",
    dbname = "postgres",
)
'''