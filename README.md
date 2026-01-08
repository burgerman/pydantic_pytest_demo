# Trade Data Enrich & Statistics Tool

Enrich trade data with feature engineering and generate summary statistics.

## Features
- **Data Enrichment**: Adds cumulative bought/sold, position, notional values, and exchange-specific metrics to the dataset.
- **Summary Statistics**: statistics output including:
  - Total shares and notional value bought and sold
  - Volume per exchange
  - Average and median fill sizes
  - Top 10 most active stocks

## Requirements
- Python 3 env

## Dependencies
Install dependencies:
   ```bash
   pip install pandas numpy pytest
   ```

## Usage
Run the script from the command line

```bash
python calc_stats/calcStats.py --inputFile=data/trades.csv --outputFile=data/enrichedTrades.csv
```

## Running Tests
Test using pytest:

```bash
python -m pytest tests/test_calc_stats.py
```
