# config.py
import os

try:
    import streamlit as st
    # ✅ Try to load from Streamlit secrets (Cloud / .streamlit/secrets.toml)
    API_KEY = st.secrets["API_KEY"]
    DB_CONFIG = {
        "host": st.secrets["DB_HOST"],
        "user": st.secrets["DB_USER"],
        "password": st.secrets["DB_PASSWORD"],
        "database": st.secrets["DB_NAME"],
        "port": int(st.secrets["DB_PORT"])
    }
except Exception:
    # ✅ Fallback for local testing (XAMPP)
    API_KEY = os.getenv("API_KEY", "Cg5QnQ4hGxac0zOPBxyZkVzuVkoEHSuAmoQ0dLiU")
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "tennis_db",
        "port": 3306
    }

# ✅ Base URL
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en"


