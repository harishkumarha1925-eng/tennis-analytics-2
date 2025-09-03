import json, os, requests
from database_handler import get_connection
from config import API_KEY, BASE_URL

DATA_DIR = "data"

# ----------------------------
# Load JSON (local file if exists, otherwise fetch from API)
# ----------------------------
def load_or_fetch(endpoint, filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        url = f"{BASE_URL}/{endpoint}?api_key={API_KEY}"
        response = requests.get(url)
        return response.json()

# ----------------------------
# Insert Categories + Competitions
# ----------------------------
def insert_categories_and_competitions():
    data = load_or_fetch("competitions.json", "competitions.json")
    conn = get_connection(); cursor = conn.cursor()

    categories = data.get("categories", [])
    competitions = data.get("competitions", [])

    for cat in categories:
        cursor.execute("INSERT IGNORE INTO Categories VALUES (%s, %s)", (cat["id"], cat["name"]))

    for comp in competitions:
        cursor.execute("""
        INSERT IGNORE INTO Competitions
        (competition_id, competition_name, parent_id, type, gender, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            comp["id"], comp["name"], comp.get("parent_id"),
            comp.get("type", ""), comp.get("gender", ""), comp["category"]["id"]
        ))

    conn.commit(); cursor.close(); conn.close()
    print(f"Inserted {len(categories)} categories and {len(competitions)} competitions.")

# ----------------------------
# Insert Complexes + Venues
# ----------------------------
def insert_complexes_and_venues():
    data = load_or_fetch("complexes.json", "complexes.json")
    conn = get_connection(); cursor = conn.cursor()

    complexes = data.get("complexes", [])
    total_venues = 0

    for complex_ in complexes:
        cursor.execute("INSERT IGNORE INTO Complexes VALUES (%s, %s)", (complex_["id"], complex_["name"]))
        for venue in complex_.get("venues", []):
            cursor.execute("""
            INSERT IGNORE INTO Venues
            (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                venue["id"], venue["name"], venue["city_name"], venue["country_name"],
                venue["country_code"], venue["timezone"], complex_["id"]
            ))
            total_venues += 1

    conn.commit(); cursor.close(); conn.close()
    print(f"Inserted {len(complexes)} complexes and {total_venues} venues.")

# ----------------------------
# Insert Competitors + Rankings
# ----------------------------
def insert_competitors_and_rankings():
    data = load_or_fetch("double_competitors_race_rankings.json", "doubles_rankings.json")
    conn = get_connection(); cursor = conn.cursor()

    groups = data.get("rankings", [])
    total_competitors, total_rankings = 0, 0

    for group in groups:
        # Some APIs wrap rankings under "competitor_rankings"
        competitors_list = group.get("competitor_rankings", [group])

        for competitor in competitors_list:
            # Extract competitor info (nested object OR flat fields)
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
            total_competitors += 1

            # Insert ranking → column is "ranking" (NOT "rank")
            cursor.execute("""
            INSERT INTO Competitor_Rankings
            (ranking, movement, points, competitions_played, competitor_id)
            VALUES (%s, %s, %s, %s, %s)
            """, (
                competitor.get("rank"),
                competitor.get("movement", 0),
                competitor.get("points", 0),
                competitor.get("competitions_played", 0),
                comp_id
            ))
            total_rankings += 1

    conn.commit(); cursor.close(); conn.close()
    print(f"Inserted {total_competitors} competitors and {total_rankings} ranking records.")

# ----------------------------
# Run All Inserts
# ----------------------------
if __name__ == "__main__":
    insert_categories_and_competitions()
    insert_complexes_and_venues()
    insert_competitors_and_rankings()
