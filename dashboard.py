import streamlit as st
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.title("💸 Real-Time Fraud Detection Dashboard")
st.markdown("Powered by Kafka, Python, and Streamlit")

# Sidebar: Refresh Interval Picker
with st.sidebar:
    st.header("⚙️ Settings")
    refresh_sec = st.slider("Refresh interval (seconds)", 2, 30, 5)

# Apply auto-refresh
st_autorefresh(interval=refresh_sec * 1000, key="auto_refresh")

log_file = "fraud_log.csv"

if not os.path.exists(log_file):
    st.warning("No fraud_log.csv found. Make sure the consumer is running.")
else:
    df = pd.read_csv(log_file)

    st.metric("🚨 Total Fraud Cases", len(df))
    st.bar_chart(df["amount"])

    # Sidebar: Type filter
    with st.sidebar:
        st.header("🔍 Filters")
        type_filter = st.text_input("Filter by transaction type")

    filtered_df = df.copy()
    if type_filter:
        filtered_df = filtered_df[filtered_df["type"].str.contains(type_filter, case=False)]

    st.subheader("📋 Recent Fraud Logs")
    st.dataframe(filtered_df.tail(20), use_container_width=True)
