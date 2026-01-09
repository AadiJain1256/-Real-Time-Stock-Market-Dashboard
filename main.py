import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")

API_KEY = "GI0KYZC3W6NUE5D2"

# stock selection
symbol = st.selectbox(
    "Select Stock Symbol",
    ["IBM", "AAPL", "MSFT", "GOOGL"]
)

@st.cache_data(ttl=300)
def fetch_stock_data(symbol):
    url = (
        "https://www.alphavantage.co/query"
        "?function=TIME_SERIES_DAILY"
        f"&symbol={symbol}"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" not in data:
        return None

    ts = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(ts, orient="index")

    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    })

    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df = df.sort_index()

    return df

df = fetch_stock_data(symbol)

if df is None:
    st.error("API limit reached or invalid response.")
else:
    fig = px.line(
        df,
        x=df.index,
        y="close",
        title=f"{symbol} Closing Price"
    )

    st.plotly_chart(fig, use_container_width=True)
