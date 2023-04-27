import yfinance as yf
import requests
from bs4 import BeautifulSoup


def grab_name(ticker):
    """grabs the name of a company given its ticker symbol"""

    stock = yf.Ticker(ticker)
    company_name = stock.info['longName']
        
   


    return company_name

# print(grab_name("AMZN"))


def grab_trending_names():
    """grabs the names of the companies with trending stocks"""

    url = 'https://finance.yahoo.com/trending-tickers'

    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table')
    headers = [th.text for th in table.find('thead').find_all('th')]

    data = []
    for tr in table.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        stock_data = [td.text.strip() for td in tds]
        stock_data.pop(-2)
        stock_data.pop(-2)
        data.append(stock_data)

    trending_names = []
    for item in data:
        trending_names.append(item[1])
    
    return trending_names


def target_stocks(ticker):

    names = []

    main = grab_name(ticker)
    trending = grab_trending_names()

    stocks = {"main":main}
    stocks["trending"] = trending
    # print(stocks)

    return stocks


def analystrt(ticker):
    """
    Return the analyst recomendation from yahoo finace 
    Based on the 
    """
    
    stock = yf.Ticker(ticker)

    # show analysts recommendations
    # stock.recommendations
    # stock.recommendations_summary
    # # show analysts other work
    # stock.analyst_price_target

    return stock.recommendations


def main():
    # ticker = "amzn"
    # stocks = target_stocks(ticker)
    # print()
    # print()
    # print()
    # print()

    # for key in stocks:
    #     print(key)
    #     print()
    #     print(stocks.get(key))
    #     print("----")
    #     print()


    print(analystrt("amzn"))

if __name__ =="__main__":
    main()