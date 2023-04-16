import yfinance as yf
msft = yf.Ticker("MSFT")
company_name = msft.info['longName']
print(company_name)