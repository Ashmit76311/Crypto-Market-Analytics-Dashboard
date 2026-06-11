# Crypto Market Analytics Dashboard

A full-stack data pipeline that ingests live cryptocurrency market data, stores it in MySQL, exposes it via a REST API, and visualizes it through interactive dashboards — all containerized with Docker.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data Ingestion | Python, Pandas, CoinGecko API |
| Database | MySQL 8 (Docker) |
| REST API | FastAPI, Uvicorn |
| Dashboards | Apache Superset |
| Reports | openpyxl (Excel) |
| Containerization | Docker, Docker Compose |

---

## Architecture

```
CoinGecko API
      │
      ▼
  ingest.py  ──────────────►  MySQL (crypto_db)
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                FastAPI         Superset        report.py
              (REST API)      (Dashboard)    (Excel Report)
            :8000/docs           :8088
```

---

## Features

- **ETL Pipeline** — Fetches top 10 coins by market cap from CoinGecko's public REST API, cleans with Pandas, inserts into MySQL
- **REST API** — 5 endpoints: list coins, price history per coin, summary stats, trigger Excel report download
- **Interactive Dashboard** — 3 charts in Apache Superset: price comparison, volume comparison, price over time
- **Excel Reports** — Auto-generated dark-themed spreadsheets with formatted currency columns
- **Docker Compose** — Single command brings up MySQL + FastAPI together

---

## Quick Start

### Prerequisites
- Docker Desktop
- Python 3.10+

### 1. Clone the repo
```bash
git clone https://github.com/Ashmit76311/crypto-tracker.git
cd crypto-tracker
```

### 2. Set up environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Start services
```bash
docker compose up -d
```

### 4. Run ingestion
```bash
python ingest.py
```

### 5. Access
| Service | URL |
|---|---|
| API Docs (Swagger) | http://localhost:8000/docs |
| Superset Dashboard | http://localhost:8088 |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/coins` | Latest snapshot for all 10 coins |
| GET | `/coins/{coin_id}/history` | Price history for a specific coin |
| GET | `/stats` | Aggregate stats across all ingested data |
| GET | `/report` | Generate and download Excel report |

---

## Project Structure

```
crypto-tracker/
├── main.py              # FastAPI application
├── ingest.py            # ETL pipeline
├── report.py            # Excel report generator
├── schema.sql           # MySQL schema
├── docker-compose.yml   # Docker services
├── requirements.txt     # Python dependencies
├── .env                 # DB credentials (not committed)
└── reports/             # Generated Excel files (not committed)
```

---

## Sample API Response

```json
GET /coins

{
  "count": 10,
  "data": [
    {
      "coin_id": "bitcoin",
      "symbol": "btc",
      "price_usd": "62744.0000000000",
      "volume_24h": "28543210000.0000",
      "market_cap": "1234567890000.0000",
      "fetched_at": "2026-06-12T00:02:52"
    }
  ]
}
```

---
