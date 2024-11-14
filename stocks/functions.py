import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
import os
import requests
import json
import matplotlib
matplotlib.use('Agg')

def plot_faang_stock(symbol, company_name):
    """
    Fetches data for the given FAANG stock symbol, plots the last 3 months of closing prices,
    and saves the graph as an image with the name 'live_<company_name>.png'.
    """
    # Fetch data for the past three months
    stock = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # Approximately three months

    # Get historical data
    hist = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    # Check if data is returned
    if hist.empty:
        print(f"No data available for {company_name} ({symbol}) in the specified period.")
        return

    # Extract dates and closing prices
    dates = hist.index
    closes = hist['Close']

    # Plot the data with a dark background
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot the line and fill the area under the line
    ax.plot(dates, closes, color="lime", linewidth=1.5, label="Close Price")
    ax.fill_between(dates, closes, color="green", alpha=0.2)

    # Set x-axis to display only month and year
    ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
    
    # Add grid lines with slight transparency for a modern look
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Set limits and customize ticks
    ax.set_ylim([min(closes) - 10, max(closes) + 10])  # Slight padding around min/max
    plt.xticks(rotation=45, ha='right')


    
    # Customize spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('gray')
    ax.spines['bottom'].set_color('gray')

    # Save the plot as an image
    filename = f'D:/Old/vscodess/django/faang/mysite/static/images/live_{company_name.lower()}.png'
    plt.savefig(filename, format="png", bbox_inches="tight", transparent=True)
    plt.close()
    print(f"Saved plot for {company_name} as '{filename}'")

# Define FAANG companies and their symbols
faang_companies = {
    "Facebook": "META",
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Netflix": "NFLX",
    "Google": "GOOGL"
}

# Generate and save plots for each FAANG company
for company, symbol in faang_companies.items():
    plot_faang_stock(symbol, company)





def fetch_data():
    """Fetch FAANG stock data from Marketstack API, cache it for the day, and return the data."""
    
    # Define the symbols for FAANG companies
    symbols = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']
    
    # Define the cache file path
    cache_file = 'faang_data_cache.json'
    
    # Check if cache exists and is valid for today
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            cache_data = json.load(file)
            # Check if the cache is from today
            if cache_data.get('date') == datetime.now().strftime('%Y-%m-%d'):
                print("Returning cached data.")
                return cache_data['data']  # Return cached data if it's from today

    # If no valid cache exists, fetch new data
    api_url = "https://api.marketstack.com/v1/eod?access_key={MARKETSTACK_API_KEY}"
    params = {
        'access_key': "MARKETSTACK_API_KEY",  # Replace with your Marketstack API key
        'symbols': ','.join(symbols)
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code != 200:
        print("Error fetching data from Marketstack API:", response.status_code)
        return None  # Return None if there's an error

    # Parse the API response
    data = response.json().get("data", [])
    
    # Process the response to extract relevant data
    faang_data = {}
    for entry in data:
        symbol = entry['symbol']
        faang_data[symbol] = {
            'date': entry['date'],
            'open': entry['open'],
            'close': entry['close'],
            'high': entry['high'],
            'low': entry['low'],
            'volume': entry['volume'],
        }
    
    # Save the data to cache with today's date
    cache_content = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'data': faang_data
    }
    
    with open(cache_file, 'w') as file:
        json.dump(cache_content, file)
    
    print("Data fetched from API and cached for the day.")
    return faang_data
