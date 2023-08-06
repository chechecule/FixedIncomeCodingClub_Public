from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np

# Chrome WebDriver 경로 설정
driver_path = 'C:/Users/dabin/Downloads/chromedriver.exe'
service = Service(driver_path)

# WebDriver 인스턴스 생성
driver = webdriver.Chrome(service=service)

url = "http://www.smbs.biz/Exchange/IRS.jsp"
driver.get(url)


# 날짜 입력 <<수정 완료 진짜..최종 ㅠ>>
date_input = driver.find_element(By.ID, 'searchDate')
driver.execute_script("arguments[0].value = '20230629';", date_input) # 조회하고 싶은 날짜 입력

# '조회하기' 버튼 클릭
search_button = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div/form/p[4]/a')
search_button.click()

# 구성 요소 조회
element = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div/form/div[9]').text

driver.quit()

lines = element.split('\n')
columns = lines[0].split()
data = [line.split() for line in lines[1:]]
df = pd.DataFrame(data, columns=columns)
#df.set_index(columns[0], inplace=True)
#위까지가 데이터 크롤링

# 테이블 구성
# Mid 값만 남기고, 2년까지만
df = df.drop(columns=["Receive","Pay"]).drop(index=df.index[5:])
# 중간테너 추가
df.index = ['1','2','3','5','7']
df.insert(0, 'Tenor',[0.5 ,0.75 ,1.00 ,1.50 ,2.00])

df.loc['0'] = [0.25,'3M', 3.75]  # 임의, 새로 크롤링한 CD로 수정할 것
df.loc['4'] = [1.25,'1.25Y',np.nan] #임의의 누락된 값 공간 생성
df.loc['6'] = [1.75,'1.75Y',np.nan] #임의의 누락된 값 공간 생성
df = df.sort_index()

# 선형 보간을 통한 값 채우기
df['Mid'] = pd.to_numeric(df['Mid'])
df2 = df.interpolate(method="linear")
#df.loc['0.25'] = [새로 크롤링한 CD] http://www.smbs.biz/Bond/BondMajor.jsp

df2['Mid'] = df2['Mid'].astype(float)


'''=========DF 추가========'''

# DF 추가
n = 4  # fixed leg: quarterly paying
DF_list = []
for i in range(8):  # df의 행 갯수가 범위가 됨
    if i <= 1:  # 3M
        DF = 1 / (1 + (df2['Mid'][i] / 100 / n))  # 1/(1+(quote*days/365))
        DF_list.append(DF)
        continue
    else:  # 6M부터 시작
        DF = (1 - (df2['Mid'][i] / 100 / n) * sum(DF_list)) / (1 + df2['Mid'][i] / 100 / n)
        DF_list.append(DF)
        continue

df2['DF'] = DF_list
df3 = df2.copy()  # df2를 복사하여 새로운 데이터프레임 생성

'''========Zero rate (continuously compounding)========'''

def GET_SR(DF,Tenor):
  return ((np.log((1/DF)))/(Tenor))*100 # DF에서 Spot rate로 변환하는 함수

df3['zero_rate_c'] = GET_SR(df3['DF'],df3['Tenor'])
    # apply함수가 적용되는 컬럼은 함수정의바디에서 파라미터와 같아야 함 !!
print(df3)



'''다음에 해야할 일
0. 수식 계산해서 맞는지 확인
1. 새로 크롤링한 CD로 수정할 것
2. implied forward rate
'''
