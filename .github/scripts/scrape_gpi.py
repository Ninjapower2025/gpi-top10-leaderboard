import requests
from bs4 import BeautifulSoup

def fetch_gpi_top30():
    url = 'https://gpimaster.com/#/group-item/1/0'  # 這是你的排行榜網址

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 這裡理論上應該找 table 但是... SPA頁面是空的
        tables = soup.find_all('table')

        if tables:
            print("找到表格啦！")
        else:
            print("❌ 找不到表格，因為是SPA網頁，HTML根本沒有資料。")
        
    else:
        print(f"網站連接失敗: {response.status_code}")

fetch_gpi_top30()
