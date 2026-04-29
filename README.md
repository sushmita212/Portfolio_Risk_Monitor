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

## How to Run End-to-End

Follow these steps to run the full pipeline from data collection to API serving.

**1. Setup environment**

The project requires Python 3.11+. It is recommended to use a virtual environment to manage dependencies.
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
- Once running, interactive API documentation is available at: /docs (Swagger UI)

## Future Work
- Implementation of Expected Shortfall (ES) as an additional tail risk measure
- Extension of the risk engine to include stress testing and scenario-based analysis
- Addition of portfolio optimization capabilities (e.g., mean-variance optimization)

