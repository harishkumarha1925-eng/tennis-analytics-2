# reset_db.py
import mysql.connector
from config import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Drop only Competitor_Rankings (safe)
cursor.execute("DROP TABLE IF EXISTS Competitor_Rankings;")

conn.commit()
cursor.close()
conn.close()

print("Competitor_Rankings table dropped ")
