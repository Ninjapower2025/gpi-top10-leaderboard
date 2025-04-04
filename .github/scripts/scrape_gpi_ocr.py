import time
import json
from playwright.sync_api import sync_playwright
from PIL import Image
import pytesseract

def scrape_top30():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://gpimaster.com/#/rank/")
        page.wait_for_timeout(10000)  # 等待網頁完全載入

        page.screenshot(path="leaderboard.png", full_page=True)
        browser.close()

    image = Image.open("leaderboard.png")
    text = pytesseract.image_to_string(image, lang="eng")

    lines = text.split("\n")
    players = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 4 and parts[0].isdigit():
            rank = int(parts[0])
            if rank > 30:
                continue
            name = parts[1]
            country = parts[2]
            score = parts[3]
            players.append({
                "rank": rank,
                "name": name,
                "country": country,
                "score": score
            })

    with open("top30.json", "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    scrape_top30()
