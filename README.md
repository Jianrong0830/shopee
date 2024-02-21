# shopee
蝦皮爬蟲

先在cmd打下面指令，會開啟一個Chrome視窗，先手動登入蝦皮然後不要關掉

cd 'YOUR_CHROME_PATH' (大多是C:\Program Files\Google\Chrome\Application)
chrome.exe --remote-debugging-port=9000 --user-data-dir="D:\selenium\AutomationProfile"

程式會用這個chrome爬取，比較不容易被發現是機器人。

有時太常爬還是會被擋，重開輸入驗證碼即可。

蝦皮圖片為動態載入，雖然已經有用滾輪，有時網路慢還是會抓不到，這時就稍微調高等待時間。