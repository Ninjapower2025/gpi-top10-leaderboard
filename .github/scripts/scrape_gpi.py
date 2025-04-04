from playwright.sync_api import sync_playwright
import json
import os

def scrape_top30():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://gpimaster.com/#/rank", timeout=60000)
        page.wait_for_timeout(5000)

        data = []
        for i in range(1, 31):
            try:
                name_selector = f'tr:nth-child({i}) td:nth-child(2)'
                country_selector = f'tr:nth-child({i}) td:nth-child(3)'
                score_selector = f'tr:nth-child({i}) td:nth-child(4)'

                name = page.locator(name_selector).inner_text()
                country = page.locator(country_selector).inner_text()
                score = float(page.locator(score_selector).inner_text())

                data.append({
                    "name": name.strip(),
                    "country": country.strip(),
                    "score": round(score, 2)
                })
            except:
                continue

        # 找到repo根目錄，正確儲存 top30.json
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_file = os.path.join(current_dir, 'top30.json')

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        browser.close()

if __name__ == "__main__":
    scrape_top30()
