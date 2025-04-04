from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime, timedelta
import time

def scrape_top30():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://gpimaster.com/#/rank", timeout=60000)

        # 等網頁完全載完
        page.wait_for_load_state('networkidle')

        # 再小等一下保險
        time.sleep(5)

        # 等表格出現
        try:
            page.wait_for_selector('table.el-table__body tbody tr', timeout=30000)
        except:
            print("⚠️ 首次未找到表格，嘗試刷新頁面...")
            page.reload()
            page.wait_for_load_state('networkidle')
            time.sleep(5)
            page.wait_for_selector('table.el-table__body tbody tr', timeout=30000)

        rows = page.locator('table.el-table__body tbody tr')
        count = rows.count()

        top30 = []
        for i in range(min(30, count)):
            row = rows.nth(i)
            cells = row.locator('td')

            try:
                player_name = cells.nth(1).inner_text().strip()
                country = cells.nth(2).inner_text().strip()
                score_text = cells.nth(4).inner_text().strip()
                score = float(score_text.replace(",", ""))

                top30.append({
                    "rank": i + 1,
                    "name": player_name,
                    "country": country,
                    "score": round(score, 2)
                })
            except Exception as e:
                print(f"Error parsing row {i+1}: {e}")
                continue

        browser.close()

        result = {
            "last_updated": (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
            "players": top30
        }

        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'top30.json')

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("✅ top30.json 已成功更新！")

if __name__ == "__main__":
    scrape_top30()

