from API.FSC import wrappers
from datetime import datetime, timedelta
# date time import

date = 2 # 이건 설정 / Day 설정
current_date = datetime.now()
#일자설정


#data = wrappers.getBondData(basDt="20230725")
#print(data.columns)
#selected_data = data[["basDt", "scrsItmsKcdNm", "bondIsurNm", "bondSrfcInrt"]]
#print(selected_data)



for i in range(date):
    t = current_date - timedelta(days=i+1)
    Dt = t.strftime("%Y%m%d")
    data = wrappers.getBondData(basDt=Dt)
    selected_data = data[["basDt", "scrsItmsKcdNm", "bondIsurNm", "bondSrfcInrt"]]
    print(selected_data)
    #데이터가 10이렇게해서 작게하면 안된다 ㅠㅠ




#a.columns
#print(a)
#a[["basDt", "scrsItmsKcdNm", "bondIsurNm", "bondSrfcInrt"]]

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