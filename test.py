import yfinance as yf

def get_ticker(company_name):
    ticker = yf.Ticker(company_name).info['symbol']
    return ticker

ticker = get_ticker("Microsoft Corporation")
print(ticker)