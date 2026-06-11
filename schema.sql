-- ============================================================
-- Crypto Tracker - Database Schema
-- Generated for: crypto-tracker project
-- Engine: MySQL 8
-- ============================================================

CREATE DATABASE IF NOT EXISTS crypto_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE crypto_db;

-- -----------------------------------------------------------
-- Table: market_data
-- Stores point-in-time price snapshots fetched from the API
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS market_data (
    id            BIGINT UNSIGNED   NOT NULL AUTO_INCREMENT,
    coin_id       VARCHAR(100)      NOT NULL COMMENT 'CoinGecko/CMC coin identifier, e.g. "bitcoin"',
    symbol        VARCHAR(20)       NOT NULL COMMENT 'Ticker symbol, e.g. "BTC"',
    price_usd     DECIMAL(28, 10)   NOT NULL COMMENT 'Current price in USD (supports micro-cap coins)',
    volume_24h    DECIMAL(28, 4)    NOT NULL COMMENT '24-hour trading volume in USD',
    market_cap    DECIMAL(28, 4)    NOT NULL COMMENT 'Market capitalisation in USD',
    fetched_at    DATETIME(3)       NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
                                    COMMENT 'UTC timestamp when this row was recorded (ms precision)',

    PRIMARY KEY (id),

    -- Speed up the most common query: latest price for a coin
    INDEX idx_coin_fetched (coin_id, fetched_at DESC),

    -- Allow fast symbol-based lookups
    INDEX idx_symbol      (symbol),

    -- Useful for time-range queries across all coins
    INDEX idx_fetched_at  (fetched_at DESC)
)
ENGINE = InnoDB
DEFAULT CHARSET = utf8mb4
COLLATE = utf8mb4_unicode_ci
COMMENT = 'Point-in-time market data snapshots for tracked cryptocurrencies';
