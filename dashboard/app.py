import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("[REDACTED]")
# PostgreSQL connection
engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/mobile_analytics"
)

st.title("Mobile Product Analytics Dashboard")

# Total users
users_query = "SELECT COUNT(*) AS total_users FROM users;"
users_df = pd.read_sql(users_query, engine)

# Total revenue
revenue_query = "SELECT ROUND(SUM(amount), 2) AS total_revenue FROM purchases;"
revenue_df = pd.read_sql(revenue_query, engine)

# Avg session length
session_query = """
SELECT ROUND(AVG(duration_minutes), 2) AS avg_session_length
FROM sessions;
"""
session_df = pd.read_sql(session_query, engine)

st.header("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Users", int(users_df.iloc[0]["total_users"]))
col2.metric("Total Revenue", f"${revenue_df.iloc[0]['total_revenue']}")
col3.metric(
    "Avg Session Length",
    f"{session_df.iloc[0]['avg_session_length']} min"
)

country_query = """
SELECT u.country,
ROUND(SUM(p.amount), 2) AS revenue
FROM users u
JOIN purchases p
ON u.user_id = p.user_id
GROUP BY u.country
ORDER BY revenue DESC;
"""

country_df = pd.read_sql(country_query, engine)

st.header("Revenue by Country")

st.bar_chart(country_df.set_index("country"))