#!/bin/bash
export PROJECT_ROOT=/Users/susmitasingh/Documents/GitHub/Portfolio_Risk_Monitor  
cd "$PROJECT_ROOT"                               # move to project root
source .venv/bin/activate                        # activate your virtual environment
python src/data/update_prices.py                 # run the Python refresh 