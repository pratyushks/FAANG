# # stocks/views.py

# from django.shortcuts import render
# from django.conf import settings
# from django.http import JsonResponse
# from django.core.cache import cache
# import requests
# import os

# def index(request):
#     # Render the main page with buttons to choose company and graph type
#     return render(request, 'stocks/index.html')

# def get_image_url(request, company, graph_type):
#     """Return the URL of the selected graph image as JSON."""
#     # Define paths to images
#     historical_images = {
#         'facebook': 'Facebook_historical_prices.png',
#         'apple': 'Apple_historical_prices.png',
#         'amazon': 'Amazon_historical_prices.png',
#         'netflix': 'Netflix_historical_prices.png',
#         'google': 'Google_historical_prices.png',
#     }

#     prediction_images = {
#         'facebook': 'Facebook_predictions.png',
#         'apple': 'Apple_predictions.png',
#         'amazon': 'Amazon_predictions.png',
#         'netflix': 'Netflix_predictions.png',
#         'google': 'Google_predictions.png',
#     }

#     # Select the correct image based on type
#     image_file = None
#     if graph_type == 'historical':
#         image_file = historical_images.get(company)
#     elif graph_type == 'prediction':
#         image_file = prediction_images.get(company)

#     # Construct full URL for the image
#     if image_file:
#         image_url = os.path.join(settings.MEDIA_URL, image_file)
#     else:
#         image_url = None

#     # Return JSON response with the image URL
#     return JsonResponse({'image_url': image_url})


# def get_faang_prices(request):
#     """Fetch or retrieve cached FAANG stock prices and graphs."""
#     # Check cache for existing data
#     faang_data = cache.get('faang_prices')
    
#     if not faang_data:
#         # Define symbols for FAANG companies
#         symbols = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']
        
#         # Marketstack API endpoint
#         api_url = f"http://api.marketstack.com/v1/eod/latest?access_key={settings.MARKETSTACK_API_KEY}&symbols={','.join(symbols)}"
        
#         # Make API request
#         response = requests.get(api_url)
        
#         if response.status_code == 200:
#             data = response.json()
#             # Process the data to get price and other necessary details
#             faang_data = {}
#             for entry in data.get("data", []):
#                 symbol = entry["symbol"]
#                 faang_data[symbol] = {
#                     "price": entry["close"],
#                     "change": entry["close"] - entry["open"],
#                     "graph_url": f"/static/images/{symbol.lower()}_graph.png"  # Placeholder graph image path
#                 }
                
#             # Cache the data for 24 hours (86400 seconds)
#             cache.set('faang_prices', faang_data, 86400)
#         else:
#             return JsonResponse({"error": "Failed to fetch stock prices"}, status=500)
    
#     return JsonResponse(faang_data)

# stocks/views.py

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.core.cache import cache
from .functions import plot_faang_stock, fetch_data
import requests
import os
from yahooquery import Screener
from django.conf import settings


def index(request):
    # Render the main page with buttons to choose company and graph type
    return render(request, 'stocks/index.html')

    if not stock_data:
        stock_data = fetch_faang_stock_data()  # Fetch data from API (or mock for now)
        cache.set('faang_stock_data', stock_data, 86400)  # Cache for 1 day (86400 seconds)
    
    return render(request, 'stocks/index.html', {'stock_data': stock_data})

def get_image_url(request, company, graph_type):
    """Return the URL of the selected graph image as JSON."""
    # Define paths to images
    historical_images = {
        'facebook': 'Facebook_historical_prices.png',
        'apple': 'Apple_historical_prices.png',
        'amazon': 'Amazon_historical_prices.png',
        'netflix': 'Netflix_historical_prices.png',
        'google': 'Google_historical_prices.png',
    }

    prediction_images = {
        'facebook': 'Facebook_predictions.png',
        'apple': 'Apple_predictions.png',
        'amazon': 'Amazon_predictions.png',
        'netflix': 'Netflix_predictions.png',
        'google': 'Google_predictions.png',
    }

    # Select the correct image based on type
    image_file = None
    if graph_type == 'historical':
        image_file = historical_images.get(company)
    elif graph_type == 'prediction':
        image_file = prediction_images.get(company)

    # Construct full URL for the image
    if image_file:
        image_url = os.path.join(settings.MEDIA_URL, image_file)
    else:
        image_url = None

    # Return JSON response with the image URL
    return JsonResponse({'image_url': image_url})

FAANG_COMPANIES = {
    "Facebook": "META",
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Netflix": "NFLX",
    "Google": "GOOGL"
}

def stock_view(request):
    # Fetch the stock data from Marketstack API
    stock_data = fetch_data()

    
    for company, symbol in FAANG_COMPANIES.items():
        plot_faang_stock(symbol, company)  # Generates and saves the plot as 'live_<company_name>.png'
    
    # Prepare data to be passed to the template
    plot_urls = {}
    for company in FAANG_COMPANIES.keys():
        company_name = company.lower()
        plot_urls[company] = {
            'image_url': f'static/images/live_{company_name}.png',  # Adjust path as necessary
            'price': stock_data[FAANG_COMPANIES[company]]['close'] if stock_data else "N/A"
        }

    # Pass plot URLs and prices to the template
    return render(request, 'stocks/stock_view.html', {'plot_urls': plot_urls})

def fetch_data():
    """Fetch live stock prices from Marketstack API."""

    url = "https://api.marketstack.com/v1/eod?access_key={settings.MARKETSTACK_API_KEY}"
    params = {
        'access_key': settings.MARKETSTACK_API_KEY,
        'symbols': ','.join(FAANG_COMPANIES.values())
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {item['symbol']: item for item in data.get('data', [])}
    except requests.RequestException as e:
        print(f"Error fetching data from Marketstack: {e}")
        return None
    
def get_live_prices(request):
    cache_key = "faang_live_prices"
    cached_data = cache.get(cache_key)

    if not cached_data:
        # Fetch new data from API and generate plots
        stock_data = fetch_data()
        if not stock_data:
            return JsonResponse({"error": "Unable to fetch stock data"}, status=500)

        plot_urls = {}
        for company, symbol in FAANG_COMPANIES.items():
            plot_faang_stock(symbol, company)  # Generates and saves 'live_<company>.png'
            company_lower = company.lower()
            plot_urls[company] = {
                'image_url': f'/static/images/live_{company_lower}.png',
                'price': stock_data[symbol]['close'] if stock_data else "N/A"
            }

        # Cache the data for one day
        cache.set(cache_key, plot_urls, 86400)  # Cache for 24 hours (86400 seconds)
    else:
        plot_urls = cached_data  # Use cached data

    return JsonResponse(plot_urls)




def fetch_top_movers():
    # Initialize the Screener object
    s = Screener()

    # Fetch top gainers
    gainers = s.get_screeners('day_gainers', count=5)['day_gainers']['quotes']

    # Fetch top losers
    losers = s.get_screeners('day_losers', count=5)['day_losers']['quotes']

    return gainers, losers

def display_stock_movers(request):
    gainers, losers = fetch_top_movers()
    return render(request, 'stocks/stocks_display.html', {'gainers': gainers, 'losers': losers})