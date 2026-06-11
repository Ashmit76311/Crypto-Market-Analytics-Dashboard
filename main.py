import os
import mysql.connector
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI(title="Crypto Market API", version="1.0.0")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "pass"),
    "database": os.getenv("DB_NAME", "crypto_db"),
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)


@app.get("/")
def root():
    return {"status": "ok", "message": "Crypto Market API is running"}


@app.get("/coins")
def get_coins():
    """Latest snapshot for all 10 coins."""
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m1.coin_id, m1.symbol, m1.price_usd, m1.volume_24h, m1.market_cap, m1.fetched_at
        FROM market_data m1
        INNER JOIN (
            SELECT coin_id, MAX(fetched_at) AS latest
            FROM market_data GROUP BY coin_id
        ) m2 ON m1.coin_id = m2.coin_id AND m1.fetched_at = m2.latest
        ORDER BY m1.market_cap DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"count": len(rows), "data": rows}


@app.get("/coins/{coin_id}/history")
def get_coin_history(coin_id: str, limit: int = 50):
    """Price history for a specific coin."""
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT coin_id, symbol, price_usd, volume_24h, fetched_at
        FROM market_data
        WHERE coin_id = %s
        ORDER BY fetched_at DESC
        LIMIT %s
    """, (coin_id, limit))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail=f"Coin '{coin_id}' not found")
    return {"coin_id": coin_id, "count": len(rows), "history": rows}


@app.get("/report")
def generate_report():
    """Trigger Excel report generation and return the file."""
    result = subprocess.run(
        ["python", "report.py"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr)

    reports_dir = "reports"
    files = sorted(os.listdir(reports_dir), reverse=True)
    if not files:
        raise HTTPException(status_code=500, detail="Report file not found")

    latest = os.path.join(reports_dir, files[0])
    return FileResponse(
        latest,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"crypto_report_{datetime.now().strftime('%Y%m%d')}.xlsx"
    )


@app.get("/stats")
def get_stats():
    """Summary stats across all ingested data."""
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            COUNT(*) AS total_records,
            COUNT(DISTINCT coin_id) AS unique_coins,
            MIN(fetched_at) AS first_ingestion,
            MAX(fetched_at) AS last_ingestion,
            MAX(price_usd) AS highest_price_seen,
            MIN(price_usd) AS lowest_price_seen
        FROM market_data
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row