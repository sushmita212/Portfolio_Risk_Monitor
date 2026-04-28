# Portfolio_Risk_Monitor
This project implements a modular risk analytics system for constructing portfolios from a configurable set of assets and computing Value-at-Risk (VaR). The portfolio is customizable through adjustable asset weights, enabling flexible risk assessment across different asset combinations.

The system is built using FastAPI to expose portfolio risk metrics through HTTP endpoints.

The primary objective of the project is to explore and apply concepts in financial risk modeling, including statistical risk estimation, model backtesting, and software engineering practices for building reliable and reproducible analytics systems. An Expected Shortfall (ES) endpoint is currently under development.

The project includes unit and integration testing to ensure correctness and reliability of the risk computation pipeline.

## System Architecture
The system computes portfolio-level Value-at-Risk (VaR) and exposes results through a FastAPI-based interface.

It is organized into four main layers:


**1. Data Layer**
- Fetches historical market data using yfinance
- Stores data locally in CSV format (data/raw/)
- Maintains metadata and refresh logs for tracking updates

  
**2. Risk Engine**
- Computes portfolio returns based on configurable asset weights
- Implements Value-at-Risk (VaR) using two approaches: Historical simulation (quantile-based method), Parametric method (Variance-Covariance approach)
- Ongoing work on implementing Expected Shortfall (ES) as an additional tail risk measure
- Supports portfolio-level aggregation across multiple assets

  
**3. API Layer**
- Built using FastAPI
- Exposes risk metrics through HTTP endpoints
- Enables programmatic access to VaR estimates for any valid portfolio configuration

  
**4. Testing Layer**
- Includes unit tests for core risk computations
- Includes integration tests for end-to-end pipeline validation
- Ensures correctness of data flow and risk calculations

## Environment Setup
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
##Data Pipeline

The system uses historical market data sourced from yfinance to construct time series for a predefined set of assets.

**Data Source**
- Historical price data is fetched using the yfinance API
- The asset universe includes liquid ETFs and indices such as SPY, QQQ, IWM, and others
**Local Storage**
- Data is stored locally in CSV format under data/raw/
- Metadata about the last update is tracked in data/metadata.json
**Data Download/Refresh**
- The dataset can be downloaded(enitre historical data)/refreshed (if some data already exists) using the update script:
```bash
scripts/update_prices.sh
```
