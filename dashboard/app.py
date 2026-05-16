import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import plotly.express as px

password = quote_plus("[REDACTED]")
# PostgreSQL connection
engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/mobile_analytics"
)

st.title("Mobile Product Analytics Dashboard")

st.sidebar.header("Dashboard Filters")

users_query = "SELECT COUNT(*) AS total_users FROM users;"
users_df = pd.read_sql(users_query, engine)


revenue_query = "SELECT ROUND(SUM(amount), 2) AS total_revenue FROM purchases;"
revenue_df = pd.read_sql(revenue_query, engine)


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

#PART 2: MONTHLY SESSION TRENDS
sessions_trend_query = """
SELECT
    DATE_TRUNC('month', session_date) AS month,
    COUNT(*) AS sessions
FROM sessions
GROUP BY month
ORDER BY month;
"""

sessions_trend_df = pd.read_sql(sessions_trend_query, engine)

st.header("Monthly Sessions Trend")

fig_sessions = px.line(
    sessions_trend_df,
    x="month",
    y="sessions",
    markers=True
)

st.plotly_chart(fig_sessions)

#PART 3: REVENUE TREND

revenue_trend_query = """
SELECT
    DATE_TRUNC('month', purchase_date) AS month,
    ROUND(SUM(amount), 2) AS revenue
FROM purchases
GROUP BY month
ORDER BY month;
"""

revenue_trend_df = pd.read_sql(revenue_trend_query, engine)

st.header("Monthly Revenue Trend")

fig_revenue = px.line(
    revenue_trend_df,
    x="month",
    y="revenue",
    markers=True
)

st.plotly_chart(fig_revenue)

#PART 4: ACQUISITION CHANNELS
channel_query = """
SELECT
    acquisition_channel,
    COUNT(*) AS users
FROM users
GROUP BY acquisition_channel
ORDER BY users DESC;
"""

channel_df = pd.read_sql(channel_query, engine)

st.header("User Acquisition Channels")

fig_channels = px.bar(
    channel_df,
    x="acquisition_channel",
    y="users"
)

st.plotly_chart(fig_channels)

#PART 5: SUBSCRIPTION BREAKDOWN

subscription_query = """
SELECT
    plan_type,
    COUNT(*) AS subscribers
FROM subscriptions
GROUP BY plan_type
ORDER BY subscribers DESC;
"""

subscription_df = pd.read_sql(subscription_query, engine)

st.header("Subscription Plan Breakdown")

fig_subs = px.pie(
    subscription_df,
    names="plan_type",
    values="subscribers"
)

st.plotly_chart(fig_subs)

#PART 6: REVENUE BY ACQUISITION CHANNEL
channel_revenue_query = """
SELECT
    u.acquisition_channel,
    ROUND(SUM(p.amount), 2) AS revenue
FROM users u
JOIN purchases p
ON u.user_id = p.user_id
GROUP BY u.acquisition_channel
ORDER BY revenue DESC;
"""

channel_revenue_df = pd.read_sql(channel_revenue_query, engine)

st.header("Revenue by Acquisition Channel")

fig_channel_revenue = px.bar(
    channel_revenue_df,
    x="acquisition_channel",
    y="revenue"
)

st.plotly_chart(fig_channel_revenue)

#PART 7: CHURN RATE QUERY
churn_query = """
SELECT
ROUND(
    COUNT(*) FILTER (
        WHERE canceled_date IS NOT NULL
    )::numeric
    / COUNT(*) * 100,
2
) AS churn_rate
FROM subscriptions;
"""

churn_df = pd.read_sql(churn_query, engine)

st.header("Subscription Churn Rate")

st.metric(
    "Churn Rate",
    f"{churn_df.iloc[0]['churn_rate']}%"
)

#PART 8: ENGAGEMENT BY COUNTRY
country_sessions_query = """
SELECT
    u.country,
    COUNT(s.session_id) AS total_sessions
FROM users u
JOIN sessions s
ON u.user_id = s.user_id
GROUP BY u.country
ORDER BY total_sessions DESC;
"""

country_sessions_df = pd.read_sql(country_sessions_query, engine)

st.header("User Engagement by Country")

fig_country_sessions = px.bar(
    country_sessions_df,
    x="country",
    y="total_sessions"
)

st.plotly_chart(fig_country_sessions)

#PART 9: TOP SUBSCRIBERS
top_spenders_query = """
SELECT
    user_id,
    ROUND(SUM(amount), 2) AS total_spent
FROM purchases
GROUP BY user_id
ORDER BY total_spent DESC
LIMIT 10;
"""

top_spenders_df = pd.read_sql(top_spenders_query, engine)

st.header("Top Spending Users")

st.dataframe(top_spenders_df)
