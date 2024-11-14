# FAANG Stock Price Prediction

## Overview

FAANG Stock Price Prediction is a Django-based web application that provides live and historical stock price data for FAANG companies (Facebook, Apple, Amazon, Netflix, and Google). Using the Marketstack API and Yahoo Finance, this application showcases current stock price movements, displays top market gainers and losers, and offers historical and predictive stock trends. The core of the predictive analysis is powered by an LSTM (Long Short-Term Memory) model, a type of neural network architecture well-suited for time-series forecasting, enabling users to view anticipated trends in FAANG stock prices.

## Features

- **Live Stock Price Display**: Real-time stock prices for each FAANG company.
- **LSTM-Powered Predictive Graphs**: Switch between historical and future projections using LSTM predictions.
- **Top Gainers and Losers**: Displays tables with the top five gainers and losers in the market.
- **Daily Data Caching**: Stock data is updated once a day to optimize API usage and reduce load times.

## Understanding the LSTM Model for Stock Prediction

LSTM (Long Short-Term Memory) networks are a class of recurrent neural networks (RNNs) specifically designed to learn from sequences of data, such as stock prices over time. LSTM is particularly advantageous for stock market prediction due to its ability to retain long-term dependencies in data sequences and mitigate the vanishing gradient problem typical in standard RNNs.

1. **Data Processing**: The LSTM model is trained on past stock prices, using historical data to learn patterns and trends.
2. **Training**: The model learns to predict future values based on historical sequences. This process includes the backpropagation of errors through time.
3. **Prediction**: Once trained, the model generates stock price forecasts, allowing the application to display predictive graphs.

## Project Structure

```
faang/
│
├── env/                     # Virtual environment
├── mysite/                  # Django project folder
│   ├── media/               # Media files (e.g., graphs and other assets)
│   ├── mysite/              # Django settings and configurations
│   ├── static/              # Static files (CSS, JS, images)
│   ├── stocks/              # Main app for handling stocks data
│   ├── .env                 # Environment variables (API keys, etc.)
│   ├── .gitignore           # Ignored files and directories
│   ├── manage.py            # Django management script
│   ├── requirements.txt     # Python dependencies
│   └── README.md            # Project documentation
```

## Setup Instructions

### Prerequisites

- **Python 3.x**
- **Pip** package installer
- **Git**
- **Marketstack API Key** (for fetching stock data)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pratyushks/FAANG.git
   cd FAANG/mysite
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows, use `env\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the `mysite/` directory with the following:
   ```bash
   MARKETSTACK_API_KEY=<your_marketstack_api_key>
   DEBUG=True  # or False in production
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

### Running the Application

To start the development server, run:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/stocks/`.

## Usage

1. **FAANG Stock Price Dashboard**:
   - On the main page, view live stock prices for each FAANG company.
   - Toggle between historical and predictive graph views for each company.

2. **Top Gainers and Losers**:
   - Use the left sidebar toggle button to view a table of the top 5 market gainers and losers.
   - This table updates daily with Yahoo Finance data.

3. **Live Stock Price Sidebar**:
   - The right sidebar toggle button reveals live stock prices along with their latest graph.

## Screenshots

### FAANG Dashboard
![Main Page](https://github.com/user-attachments/assets/bbc3b778-8c86-4574-bf8e-b41a274b0da4)

### Historical Graph
![Historic Graph](https://github.com/user-attachments/assets/46763b51-bc13-4f5e-a93f-f3b401b321ad)

### Predictive LSTM Graph
![Prediction Graph](https://github.com/user-attachments/assets/7796ed04-0a74-4ffa-88d2-7493581c54ec)

### Right Sidebar with Live Prices
![Right Sidebar](https://github.com/user-attachments/assets/bdfe21e6-bfbb-4e7c-a7c0-7cad730bb177)

### Left Sidebar with Top Movers
![Left Sidebar](https://github.com/user-attachments/assets/7da10797-f7e7-48fb-a3fb-511b9d102614)
