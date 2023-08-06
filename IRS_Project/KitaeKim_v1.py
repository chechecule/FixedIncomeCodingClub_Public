# 우클릭이 안되어서... 재화 아이디어를 바탕으로 selenium으로 크롬을 직접 컨트롤하는 프로그래밍을 했습니다. XPATH 기반으로 클릭과 키 입력을 해봤어요.
# 당일의 표 복사 및 n-1일 전 데이터까지 dataframe형식으로 저장하는 코드입니다.
# Mid값만 취하고 Receive Pay 값은 일단 버렸습니다.
# 데이터 로딩이 느리면 time_lag 변수를 올려주시고 탐색할 일자를 변경하려면 n을 조정해주세요
# 부족한 부분이나 아이디어 있으면 말씀주셔요~

#%% SMB 크롤링~


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import pandas as pd
import time

driver = webdriver.Chrome('D:/Data/python/chromedriver.exe') 
url = "http://www.smbs.biz/Exchange/IRS.jsp"  
driver.get(url)
df = pd.DataFrame()
start_date = datetime.today()

n = 5 # 탐색할 일자(휴일 포함)
time_lag = 1 # 로딩 시간 조절

for _ in range(n):
    date_element = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div/form/div[6]/table/tbody/tr/td/input")
    for _ in range(8):
        date_element.send_keys(Keys.BACKSPACE)
    start_date_str = start_date.strftime('%Y%m%d')
    driver.execute_script(f"arguments[0].value = '{start_date_str}';", date_element)
    inquire_botton = driver.find_element(by = By.XPATH, value = '/html/body/div/div[4]/div[2]/div/form/p[4]/a/img')
    inquire_botton.click()
    time.sleep(time_lag) 
    table_html = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div/form/div[9]/table").get_attribute('outerHTML')
    data = pd.read_html(table_html)
    data = data[0] 
    data.columns = data.columns.str.replace(r'.*;', '', regex=True)
    data.replace(to_replace=r'.*;', value='', regex=True, inplace=True)
    
    data_mid = data[['기일물', 'Mid']] 
    data_mid.rename(columns={'Mid': start_date_str, '기일물':'Tenors'}, inplace=True) # start_date를 열 이름으로 대체
    data_mid.set_index('Tenors', inplace=True) # Tenors 인덱스 설정
    df = pd.concat([df, data_mid], axis=1) # 수평으로 합치기

    start_date = datetime.strptime(start_date_str,'%Y%m%d')
    start_date = start_date - timedelta(days=1)

driver.quit()

df.to_excel('irs_output.xlsx', index=True) 
print(df)
