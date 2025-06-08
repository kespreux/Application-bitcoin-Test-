# Bitcoin Price Stats

This package periodically fetches Bitcoin price data from the [CoinGecko API](https://www.coingecko.com/en/api) and displays rolling statistics.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the tracker:
   ```bash
   python -m bitcoin_stats.main
   ```

The console will update every second with the current BTC price and summary statistics for the last hour, 24 hours and 30 days.
