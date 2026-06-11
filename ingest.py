import os
import requests
import pandas as pd
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "pass"),
    "database": os.getenv("DB_NAME", "crypto_db"),
}

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order":       "market_cap_desc",
    "per_page":    10,
    "page":        1,
    "sparkline":   False,
}

# --- Fetch ---
def fetch_data() -> pd.DataFrame:
    print(f"[{datetime.now()}] Fetching from CoinGecko...")
    response = requests.get(COINGECKO_URL, params=PARAMS, timeout=10)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data)[["id", "symbol", "current_price", "total_volume", "market_cap"]]
    df.rename(columns={
        "id":            "coin_id",
        "current_price": "price_usd",
        "total_volume":  "volume_24h",
    }, inplace=True)

    df["price_usd"]  = pd.to_numeric(df["price_usd"],  errors="coerce").fillna(0)
    df["volume_24h"] = pd.to_numeric(df["volume_24h"], errors="coerce").fillna(0)
    df["market_cap"] = pd.to_numeric(df["market_cap"], errors="coerce").fillna(0)

    print(f"  Fetched {len(df)} coins.")
    return df

# --- Insert ---
def insert_data(df: pd.DataFrame):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
        INSERT INTO market_data (coin_id, symbol, price_usd, volume_24h, market_cap)
        VALUES (%s, %s, %s, %s, %s)
    """
    rows = [
        (row.coin_id, row.symbol, float(row.price_usd),
         float(row.volume_24h), float(row.market_cap))
        for row in df.itertuples(index=False)
    ]

    cursor.executemany(sql, rows)
    conn.commit()
    print(f"  Inserted {cursor.rowcount} rows.")

    cursor.close()
    conn.close()

# --- Run ---
if __name__ == "__main__":
    df = fetch_data()
    insert_data(df)
    print("Done.")