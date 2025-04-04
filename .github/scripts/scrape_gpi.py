from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime, timedelta

def scrape_top30():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 打開 gpimaster 排行榜
        page.goto("https://gpimaster.com/#/rank", timeout=60000)

        # 等待主要表格載入
        page.wait_for_selector('table.el-table__body tbody tr', timeout=15000)

        # 爬取前30行的數據
        rows = page.locator('table.el-table__body tbody tr')
        count = rows.count()

        top30 = []
        for i in range(min(30, count)):
            row = rows.nth(i)
            cells = row.locator('td')

            try:
                # 第二格是玩家姓名
                player_name = cells.nth(1).inner_text().strip()
                # 第三格是國家
                country = cells.nth(2).inner_text().strip()
                # 第五格是積分
                score_text = cells.nth(4).inner_text().strip()
                score = float(score_text.replace(",", ""))  # 去掉千位逗號

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

        # 保存為 JSON
        result = {
            "last_updated": (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
            "players": top30
        }

        # 定位到 repo 頂層的 top30.json
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'top30.json')

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("✅ top30.json 已成功更新！")

if __name__ == "__main__":
    scrape_top30()
