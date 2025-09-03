import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categories (
        category_id VARCHAR(50) PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Competitions (
        competition_id VARCHAR(50) PRIMARY KEY,
        competition_name VARCHAR(100) NOT NULL,
        parent_id VARCHAR(50),
        type VARCHAR(20) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        category_id VARCHAR(50),
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Complexes (
        complex_id VARCHAR(50) PRIMARY KEY,
        complex_name VARCHAR(100) NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Venues (
        venue_id VARCHAR(50) PRIMARY KEY,
        venue_name VARCHAR(100) NOT NULL,
        city_name VARCHAR(100) NOT NULL,
        country_name VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        timezone VARCHAR(100) NOT NULL,
        complex_id VARCHAR(50),
        FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Competitors (
        competitor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        abbreviation VARCHAR(10) NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Competitor_Rankings (
        rank_id INT AUTO_INCREMENT PRIMARY KEY,
        rank INT NOT NULL,
        movement INT NOT NULL,
        points INT NOT NULL,
        competitions_played INT NOT NULL,
        competitor_id VARCHAR(50),
        FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
    )""")

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
