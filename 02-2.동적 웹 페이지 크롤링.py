from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# [CODE 1]
def CoffeeBean_store(result):
    CoffeeBean_URL = "https://www.coffeebeankorea.com/store/store.asp"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 브라우저를 숨김 모드로 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    for page in range(1, 370):  # 매장 수만큼 반복
        wd.get(CoffeeBean_URL)
        time.sleep(1)  # 웹페이지 연결할 동안 1초 대기
        try:
            wd.execute_script("storePop2(%d)" % page)  # page 인덱스를 페이지 번호로 사용
            time.sleep(1)  # 스크립트 실행할 동안 1초 대기
            html = wd.page_source
            soupCB = BeautifulSoup(html, 'html.parser')
            store_name_h2 = soupCB.select("div.store_txt > h2")
            store_name = store_name_h2[0].string
            print(store_name)  # 매장 이름 출력하기
            store_info = soupCB.select("div.store_txt > table.store_table > tbody > tr > td")
            store_address_list = list(store_info[2])
            store_address = store_address_list[0]
            store_phone = store_info[3].string
            result.append([store_name, store_address, store_phone])
        except Exception as e:
            print(e)
            continue
    wd.quit()
    return

# [CODE 0]
def main():
    result = []
    print('CoffeeBean store crawling >>>>>>>>>>>>>>>>>>')
    CoffeeBean_store(result)  # [CODE 1]

    CB_tbl = pd.DataFrame(result, columns=('store', 'address', 'phone'))  # columns로 수정
    CB_tbl.to_csv('./CoffeeBean.csv', encoding='cp949', mode='w', index=True)

if __name__ == '__main__':
    main()
