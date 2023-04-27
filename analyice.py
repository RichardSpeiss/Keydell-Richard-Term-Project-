# import pandas as pd
# import yfinance as yf

# # Define the list of tickers to retrieve ratings for
# tickers = ['AAPL', 'MSFT', 'GOOG']

# # Fetch the ratings data using Yahoo Finance
# ratings_data = yf.download(tickers, group_by='ticker', actions=True)

# # Extract the analyst ratings from the ratings data
# ratings = ratings_data['Recommendation Mean']
# print(ratings_data.columns)


# # Print the ratings DataFrame
# print(ratings)





import requests

# Replace YOUR_API_KEY with your actual Alpha Vantage API key
API_KEY = 'YOUR_API_KEY'
symbol = 'AAPL' # replace AAPL with your desired stock symbol

url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'

response = requests.get(url)
data = response.json()

rating = data['AnalystRating']

print(f'The analyst rating for {symbol} is {rating}.')
