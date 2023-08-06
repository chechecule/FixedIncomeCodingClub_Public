from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Chrome WebDriver 경로 설정
driver_path = 'C:/Users/dabin/Downloads/chromedriver.exe'
service = Service(driver_path)

# WebDriver 인스턴스 생성
driver = webdriver.Chrome(service=service)

url = "http://www.smbs.biz/Exchange/IRS.jsp"
driver.get(url)

# 날짜 입력
date_input = driver.find_element(By.ID, 'searchDate')
date_input.clear()
date_input.send_keys('20230621')  # 조회하고 싶은 날짜 입력

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
df.set_index(columns[0], inplace=True)

print(df)
