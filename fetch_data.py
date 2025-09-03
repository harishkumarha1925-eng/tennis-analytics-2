import json, os, requests
from database_handler import get_connection
from config import API_KEY, BASE_URL

DATA_DIR = "data"

def load_or_fetch(endpoint, filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        url = f"{BASE_URL}/{endpoint}?api_key={API_KEY}"
        return requests.get(url).json()

def insert_categories_and_competitions():
    data = load_or_fetch("competitions.json", "competitions.json")
    conn = get_connection(); cursor = conn.cursor()
    for cat in data.get("categories", []):
        cursor.execute("INSERT IGNORE INTO Categories VALUES (%s, %s)", (cat["id"], cat["name"]))
    for comp in data.get("competitions", []):
        cursor.execute("INSERT IGNORE INTO Competitions VALUES (%s, %s, %s, %s, %s, %s)",
                       (comp["id"], comp["name"], comp.get("parent_id"),
                        comp.get("type", ""), comp.get("gender", ""), comp["category"]["id"]))
    conn.commit(); cursor.close(); conn.close()
    print("Competitions & Categories inserted.")

def insert_complexes_and_venues():
    data = load_or_fetch("complexes.json", "complexes.json")
    conn = get_connection(); cursor = conn.cursor()
    for complex_ in data.get("complexes", []):
        cursor.execute("INSERT IGNORE INTO Complexes VALUES (%s, %s)", (complex_["id"], complex_["name"]))
        for venue in complex_.get("venues", []):
            cursor.execute("INSERT IGNORE INTO Venues VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (venue["id"], venue["name"], venue["city_name"], venue["country_name"],
                            venue["country_code"], venue["timezone"], complex_["id"]))
    conn.commit(); cursor.close(); conn.close()
    print("Complexes & Venues inserted.")

def insert_competitors_and_rankings():
    data = load_or_fetch("double_competitors_race_rankings.json", "doubles_rankings.json")
    conn = get_connection(); cursor = conn.cursor()

    # Some APIs wrap rankings inside "rankings" -> "competitor_rankings"
    for group in data.get("rankings", []):
        competitors_list = group.get("competitor_rankings", [group])  # fallback: direct list

        for competitor in competitors_list:
            # Handle nested competitor object or flat fields
            if "competitor" in competitor:
                comp = competitor["competitor"]
                comp_id = comp.get("id")
                name = comp.get("name")
                country = comp.get("country")
                country_code = comp.get("country_code")
                abbreviation = comp.get("abbreviation", "")
            else:
                comp_id = competitor.get("competitor_id")
                name = competitor.get("competitor_name")
                country = competitor.get("country")
                country_code = competitor.get("country_code")
                abbreviation = competitor.get("abbreviation", "")

            # Insert competitor
            cursor.execute("""
            INSERT IGNORE INTO Competitors (competitor_id, name, country, country_code, abbreviation)
            VALUES (%s, %s, %s, %s, %s)
            """, (comp_id, name, country, country_code, abbreviation))

            # Insert ranking (with safe .get())
            cursor.execute("""
            INSERT INTO Competitor_Rankings (rank, movement, points, competitions_played, competitor_id)
            VALUES (%s, %s, %s, %s, %s)
            """, (
                competitor.get("rank"),
                competitor.get("movement", 0),
                competitor.get("points", 0),
                competitor.get("competitions_played", 0),
                comp_id
            ))

    conn.commit(); cursor.close(); conn.close()
    print("Competitors & Rankings inserted.")



if __name__ == "__main__":
    insert_categories_and_competitions()
    insert_complexes_and_venues()
    insert_competitors_and_rankings()
