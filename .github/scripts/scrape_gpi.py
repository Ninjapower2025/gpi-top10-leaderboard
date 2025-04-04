import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_top30():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://gpimaster.com/#/rank/', timeout=60000)

        # 等待表格出現
        await page.wait_for_selector("table.el-table__body tbody tr")

        rows = await page.query_selector_all("table.el-table__body tbody tr")
        
        results = []

        for row in rows[:30]:  # 抓前30名
            cols = await row.query_selector_all('td')
            if len(cols) >= 5:
                rank = (await cols[0].inner_text()).strip()
                name = (await cols[1].inner_text()).strip()
                country = (await cols[2].inner_text()).strip()
                score = (await cols[4].inner_text()).strip()
                results.append({
                    "rank": rank,
                    "name": name,
                    "country": country,
                    "score": score
                })

        # 正確儲存為 top30.json （不是 top30_final.json）
        with open('top30.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_top30())
