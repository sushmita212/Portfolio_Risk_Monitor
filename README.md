# Portfolio Risk Monitor
This project implements a modular risk analytics system for constructing portfolios from a configurable set of assets and computing Value-at-Risk (VaR). The portfolio is customizable through adjustable asset weights, enabling flexible risk assessment across different asset combinations.

The system is built using FastAPI to expose portfolio risk metrics through HTTP endpoints.

The primary objective of the project is to explore and apply concepts in financial risk modeling, including statistical risk estimation, model backtesting, and software engineering practices for building reliable and reproducible analytics systems. 

The project includes unit and integration testing to ensure correctness and reliability of the risk computation pipeline.

## System Architecture
The system follows a sequential pipeline that transforms raw market data into portfolio-level Value-at-Risk (VaR) estimates exposed via a FastAPI interface.
**Pipeline Overview**
```text
Market Data (yfinance)
        ↓
Data Layer (download + refresh CSV storage)
        ↓
Feature Layer (asset returns computation)
        ↓
Portfolio Layer (weighted aggregation, stats)
        ↓
Risk Engine (VaR: Historical + Parametric)
        ↓
API Layer (FastAPI endpoints)
        ↓
User
```
**Testing Layer**
- Used to validate all components of the pipeline
- Covers returns computation, portfolio logic, and VaR calculations



## Data Pipeline

The system uses historical market data sourced from yfinance to construct time series for a predefined set of assets.

**Data Source**
- Historical price data is fetched using the yfinance API
- The asset universe includes liquid ETFs and indices such as SPY, QQQ, IWM, and others
  
**Local Storage**
- Data is stored locally in CSV format under data/raw/
- Metadata about the last update is tracked in data/metadata.json, and refresh activity is logged in logs/refresh.jsonl
  
**Data Download/Refresh**
- The dataset can be fully downloaded (initial run) or incrementally refreshed (subsequent runs) using the update script:
```bash
scripts/update_prices.sh
```
## Risk Layer

The risk layer is responsible for computing portfolio-level risk metrics from historical asset price data.

**Portfolio Construction**
- Portfolio returns are constructed using user-defined asset weights
- Returns are aggregated across multiple assets to form a single portfolio return series

**Risk Estimation Methods**

The system implements VaR using two approaches:

- Historical Simulation (Quantile-Based Method):
VaR is computed directly from the empirical distribution of historical portfolio returns.
- Parametric (Variance-Covariance Method):
VaR is estimated under a normality assumption using portfolio mean and covariance of returns.

**Output**

The layer produces portfolio-level VaR estimates for a given confidence level and time horizon

## API Layer

The system exposes portfolio risk metrics through a FastAPI-based REST interface.

**Functionality**
- Provides programmatic access to VaR estimates
- Accepts portfolio configuration inputs (asset tickers, weights, time horizon, confidence level, VaR method, and drift inclusion flag)
- Returns computed risk metrics in JSON format
  
**Usage**

The API can be started using:

```bash
uvicorn src.api.main:app --reload
```
Once running, interactive API documentation is available at: /docs (Swagger UI)

## How to Run End-to-End

Follow these steps to run the full pipeline from data collection to API serving.

**1. Setup environment**
The project requires Python 3.11+.

It is recommended to use a virtual environment to manage dependencies.
```bash
# Clone the repository
git clone <repo-url>
cd Portfolio_Risk_Monitor

# Create virtual environment
python3 -m venv venv

# Activate environment
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
**2. Download / refresh data**
```bash
scripts/update_prices.sh
```
**3. Start the API**
```bash
uvicorn src.api.main:app --reload
```
**4. Access API**
- Swagger UI: http://127.0.0.1:8000/docs


## Future Work
- Implementation of Expected Shortfall (ES) as an additional tail risk measure
- Extension of the risk engine to include stress testing and scenario-based analysis
- Addition of portfolio optimization capabilities (e.g., mean-variance optimization)

