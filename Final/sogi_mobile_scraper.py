from importlib.resources import path
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import pandas as pd

delay_time = 1

def main():
    opts = Options() 
    opts.add_argument('--log-level=3') 
    opts.add_argument('--headless') 
    opts.add_argument('--disable-gpu') 

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s,options=opts)
    driver.set_window_size(1440, 900)

    # Construct a directory to store the data
    if not os.path.exists('sogi_data'):
        os.mkdir('sogi_data')

    # Crawling
    url_cellphones = 'https://www.sogi.com.tw/search/cellphone/'
    driver.get(url_cellphones)

    time.sleep(delay_time)
    url_list = driver.find_elements(By.CLASS_NAME, 'text-row-2')
    url_list = [m.get_attribute('href') for m in url_list]
    
    print('---------------------------------')
    print('Num. of cellphone =', len(url_list))

    beg = int(input('Enter the beg(min: 1): ')) - 1
    end = int(input('Enter the end(max:'+str(len(url_list))+'): '))

    print()

    # Scraping for each cellphone
    for i, url in enumerate(url_list[beg:end]):
        print('[' + str(i+1)+'/'+ str(end-beg)+ '] ' + url.split('/')[-2])
        driver.get(url)

        time.sleep(delay_time)
        price = driver.find_elements(By.XPATH, '//*[@id="main"]/div[2]/div[4]/div/div/div[2]/div/div[3]/div/div/div[2]/a/div[1]')
        if len(price):
            price = price[0].text
        else:
            with open('sogi\\log.txt', 'a') as f:
                f.write(url)
            continue

        driver.find_elements(By.XPATH, '//*[@id="spec"]/div/div[1]/div/div[2]/a')[0].click()
        time.sleep(delay_time)
        trlist = driver.find_elements(By.TAG_NAME, 'tr')
        time.sleep(delay_time)
        df = pd.DataFrame([price], columns=['Price'])
        for row in trlist:
            th = row.find_elements(By.TAG_NAME, 'th')
            td = row.find_elements(By.TAG_NAME, 'td')
            if len(td):
                df[th[0].text] = td[0].text

        df.to_csv(os.path.join('sogi_data', url.split('/')[-2]+'.csv'), index=False)

if __name__ == '__main__':
    main()