'''
先在cmd打這個，會開啟一個Chrome視窗，先手動登入蝦皮然後不要關掉
cd C:\Program Files\Google\Chrome\Application
chrome.exe --remote-debugging-port=9000 --user-data-dir="D:\selenium\AutomationProfile"
'''

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

def scrape_shopee_shop(shop_url):
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9000")
    driver = webdriver.Chrome(options=options)

    driver.get(shop_url)
    time.sleep(5)  # 等待頁面初次加載

    page = 1
    none_cnt = 0
    item_count = 1  # 初始化商品序號
    prev_products = None  # 初始化上一頁的商品
    data = []

    while True:
        time.sleep(2)  # 等待頁面商品加載
        driver.execute_script("window.scrollTo(0, 0);")  # 滾動到頁面頂部
        time.sleep(2)  # 等待頁面商品加載
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(2)  # 等待頁面商品加載
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)  # 等待頁面商品加載
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4*3);")
        time.sleep(2)  # 等待頁面商品加載
        driver.find_element_by_tag_name('body').send_keys(Keys.END)  # 滾動到頁面底部
        time.sleep(2)
        
        try:
            # 獲取當前頁面的HTML源碼
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            # 查找所有商品標題
            products = soup.find_all('div', class_='shop-search-result-view__item col-xs-2-4')
    
            # 比較當前頁面的商品與上一頁的商品是否相同
            if prev_products and products == prev_products:
                # 如果相同，則停止爬取
                break
    
            prev_products = products
    
            for product in products:
                title = product.find('div', class_='ZAlrfe OyGzKs aaYMoU').text
                price = product.find('span', class_='F-wiHG').text
                link = "https://shopee.tw/" + product.find('a')['href']
                img = product.find('img', class_='BxUpkW xB+NXl')
                if img is not None:
                    img = img['src']
                else:
                    img = None
                    none_cnt += 1
    
                data.append({
                    '編號': item_count,
                    '標題': title,
                    '價格': price,
                    '商品網址': link,
                    '圖片網址': img
                })
                
                print(f"{item_count}. {title}")
                print('價格：', price)
                print('商品網址：', link)
                print('圖片網址：', img)
                print()
    
                item_count += 1  # 商品序號加1
            
            print(f"第 {page} 頁， 圖片未加載數量： {none_cnt}")
            print()
            page += 1
            
            # 點擊下一頁按鈕
            next_button = driver.find_element_by_css_selector('.shopee-icon-button.shopee-icon-button--right')
            next_button.click()
        except Exception  as err:
            print(err)
            break

    driver.quit()

    return data

shops = ['hanktown', 'go_wild', 'sanminbook']

for shop in shops:
    print("正在爬取", shop)
    url = 'https://shopee.tw/' + shop + '?is_from_login=true#product_list'
    data = scrape_shopee_shop(url)
    df = pd.DataFrame(data)
    df.to_csv(f'{shop}.csv', index=False, encoding='utf-8-sig')
