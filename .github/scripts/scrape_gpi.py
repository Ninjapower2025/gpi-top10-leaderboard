from playwright.sync_api import sync_playwright
import easyocr
import json
import os
from datetime import datetime, timedelta
from PIL import Image

def scrape_gpi_ocr():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 打開gpimaster排行榜頁
        page.goto("https://gpimaster.com/#/rank", timeout=60000)
        
        # 等待網頁載入完成
        page.wait_for_load_state('networkidle')
        
        # 延遲確保內容渲染完成
        page.wait_for_timeout(5000)
        
        # 對整個畫面截圖
        screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gpi_screenshot.png")
        page.screenshot(path=screenshot_path, full_page=True)
        
        browser.close()

    # 用EasyOCR讀取截圖
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=False)
    result = reader.readtext(screenshot_path, detail=0)

    # 處理OCR結果
    players = []
    temp_player = {}
    count = 0
    for text in result:
        text = text.strip()
        if text.isdigit() and 1 <= int(text) <= 30:
            if temp_player:
                players.append(temp_player)
                temp_player = {}
            temp_player['rank'] = int(text)
            count = 1
        elif count == 1:
            temp_player['name'] = text
            count = 2
        elif count == 2:
            temp_player['country'] = text
            count = 3
        elif count == 3:
            try:
                temp_player['score'] = float(text.replace(",", ""))
            except:
                temp_player['score'] = 0.0
            players.append(temp_player)
            temp_player = {}
            count = 0

    if temp_player:
        players.append(temp_player)

    # 只保留前30名
    players = players[:30]

    # 儲存成JSON
    data = {
        "last_updated": (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
        "players": players
    }

    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "top30_final.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ top30_final.json 已生成完成！")

if __name__ == "__main__":
    scrape_gpi_ocr()
