import streamlit as st
import pandas as pd
from database_handler import get_connection
import queries as q

st.set_page_config(page_title="🎾 Tennis Analytics", layout="wide")
st.title("🎾 Game Analytics: Unlocking Tennis Data")

def run_query(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# KPIs
st.subheader("📊 Dashboard")
col1, col2, col3 = st.columns(3)
total_competitors = run_query("SELECT COUNT(*) as count FROM Competitors")["count"][0]
total_countries = run_query("SELECT COUNT(DISTINCT country) as count FROM Competitors")["count"][0]
highest_points = run_query("SELECT MAX(points) as max_points FROM Competitor_Rankings")["max_points"][0]
col1.metric("Total Competitors", total_competitors)
col2.metric("Countries Represented", total_countries)
col3.metric("Highest Points", highest_points)

# Leaderboard
st.subheader("🏆 Top Ranked Competitors")
st.dataframe(run_query(q.TOP_RANKED_COMPETITORS))

# Search
st.subheader("🔍 Search Competitor")
search = st.text_input("Enter competitor name:")
if search:
    df_search = run_query("""
    SELECT c.name, c.country, r.rank, r.points, r.movement, r.competitions_played
    FROM Competitor_Rankings r
    JOIN Competitors c ON c.competitor_id = r.competitor_id
    WHERE c.name LIKE %s
    """, (f"%{search}%",))
    st.dataframe(df_search)

# Country analysis
st.subheader("🌍 Country-Wise Analysis")
st.dataframe(run_query(q.COUNTRY_ANALYSIS))
