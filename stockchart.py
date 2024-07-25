
import os
import requests
import matplotlib.pyplot as plt
import pandas as pd
#from dotenv import load_dotenv
import datetime as dt
import matplotlib.dates as mdates

# Load environment variables from .env file
#oad_dotenv()

# Get the Alpha Vantage API key from environment variables
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# Stock symbol you want to fetch data for
stock_symbol = input("key in the stock of your choice: ")

# Function to fetch historical stock data from Alpha Vantage
def get_stock_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['Time Series (Daily)']

# Fetch historical data
stock_data = get_stock_data(stock_symbol, api_key)

# Prepare data for the candlestick chart
data = []
for date, values in stock_data.items():
    data.append([dt.datetime.strptime(date, '%Y-%m-%d'),
                 float(values['1. open']),
                 float(values['2. high']),
                 float(values['3. low']),
                 float(values['4. close'])])

data.sort(key=lambda x: x[0])  # Sort data by date

# Create DataFrame
df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
df.set_index('Date', inplace=True)

# Plot candlestick chart
fig, ax = plt.subplots(figsize=(10, 5))

# Define the width of candlesticks
width = 0.6
width2 = 0.1

# Define colors
up = df[df['Close'] >= df['Open']]
down = df[df['Close'] < df['Open']]

col1 = 'green'
col2 = 'red'

# Plot data
ax.bar(up.index, up['Close']-up['Open'], width, bottom=up['Open'], color=col1)
ax.bar(up.index, up['High']-up['Close'], width2, bottom=up['Close'], color=col1)
ax.bar(up.index, up['Low']-up['Open'], width2, bottom=up['Open'], color=col1)

ax.bar(down.index, down['Close']-down['Open'], width, bottom=down['Open'], color=col2)
ax.bar(down.index, down['High']-down['Open'], width2, bottom=down['Open'], color=col2)
ax.bar(down.index, down['Low']-down['Close'], width2, bottom=down['Close'], color=col2)

# Format the x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.xticks(rotation=45)

# Set titles and labels
plt.title(f'{stock_symbol} Candlestick Chart')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.tight_layout()
plt.show()