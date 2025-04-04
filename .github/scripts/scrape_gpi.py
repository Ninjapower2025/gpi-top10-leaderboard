import requests
import json
import os
from datetime import datetime, timedelta

def scrape_top30():
    url = "https://gpimaster.com/api/rank"
    response = requests.get(url)

    if response.status_code == 200:
        full_data = response.json()
        
        # 只取前30名
        top30 = []
        for i, player in enumerate(full_data[:30]):
            top30.append({
                "rank": i + 1,
                "name": player.get("playerName", ""),
                "country": player.get("country", ""),
                "score": round(player.get("score", 0), 2)
            })

        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_file = os.path.join(current_dir, 'top30.json')

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "last_updated": (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                "players": top30
            }, f, ensure_ascii=False, indent=2)

        print("Successfully updated top30.json!")

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_top30()
