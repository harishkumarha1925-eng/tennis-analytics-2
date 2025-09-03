import requests, json, os
from config import API_KEY, BASE_URL

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_json(endpoint, filename):
    url = f"{BASE_URL}/{endpoint}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4)
        print(f"Saved {filename}")
    else:
        print(f"Failed {endpoint} - Status {response.status_code}")  # 👈 simple text only

if __name__ == "__main__":
    save_json("competitions.json", "competitions.json")
    save_json("complexes.json", "complexes.json")
    save_json("double_competitors_race_rankings.json", "doubles_rankings.json")



