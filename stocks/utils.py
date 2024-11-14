# utils.py

import requests
from django.conf import settings

def fetch_faang_stock_data():
    api_key = settings.MARKETSTACK_API_KEY
    symbols = ['AAPL', 'META', 'AMZN', 'NFLX', 'GOOGL']
    url = f"http://api.marketstack.com/v1/eod/latest"
    params = {
        'access_key': api_key,
        'symbols': ','.join(symbols)
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    stock_data = {}
    for stock in data['data']:
        symbol = stock['symbol']
        company_name = {
            'AAPL': 'Apple',
            'META': 'Facebook',
            'AMZN': 'Amazon',
            'NFLX': 'Netflix',
            'GOOGL': 'Google'
        }.get(symbol, 'Unknown')
        
        stock_data[company_name] = {
            'price': stock['close'],
            'graph_url': f'static/images/live_{company_name.lower()}.png'
        }
    
    return stock_data
