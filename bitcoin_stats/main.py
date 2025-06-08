import time
import requests
from collections import deque
from datetime import datetime

ONE_HOUR = 3600
ONE_DAY = 86400
THIRTY_DAYS = 30 * ONE_DAY

# Store (timestamp, price) tuples for the last 30 days
price_history = deque(maxlen=THIRTY_DAYS)

API_URL = 'https://api.coingecko.com/api/v3/simple/price'
PARAMS = {'ids': 'bitcoin', 'vs_currencies': 'usd'}


def fetch_price():
    """Fetch current BTC price in USD from CoinGecko."""
    response = requests.get(API_URL, params=PARAMS, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data['bitcoin']['usd']


def summarize(seconds):
    """Return (avg, high, low) for entries within the last `seconds`."""
    cutoff = time.time() - seconds
    prices = [price for ts, price in price_history if ts >= cutoff]
    if not prices:
        return None
    avg = sum(prices) / len(prices)
    high = max(prices)
    low = min(prices)
    return avg, high, low


def display(current_price):
    hour_stats = summarize(ONE_HOUR)
    day_stats = summarize(ONE_DAY)
    month_stats = summarize(THIRTY_DAYS)

    def fmt(stats):
        if not stats:
            return 'n/a', 'n/a', 'n/a'
        return (f"{stats[0]:.2f}", f"{stats[1]:.2f}", f"{stats[2]:.2f}")

    hour_avg, hour_high, hour_low = fmt(hour_stats)
    day_avg, day_high, day_low = fmt(day_stats)
    month_avg, month_high, month_low = fmt(month_stats)

    print("\033c", end="")
    print(f"{datetime.now().isoformat()} - Current BTC price: ${current_price:.2f}")
    print()
    print("Timeframe        Average     High        Low")
    print("-" * 44)
    print(f"Last hour        {hour_avg:>8}    {hour_high:>8}    {hour_low:>8}")
    print(f"Last 24h         {day_avg:>8}    {day_high:>8}    {day_low:>8}")
    print(f"Last 30d         {month_avg:>8}    {month_high:>8}    {month_low:>8}")


def main():
    while True:
        try:
            price = fetch_price()
            price_history.append((time.time(), price))
            display(price)
        except Exception as e:
            print(f"Error fetching price: {e}")
        time.sleep(1)


if __name__ == '__main__':
    main()
