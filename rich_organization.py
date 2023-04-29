from newsapi.newsapi_client import NewsApiClient
from flair.models import TextClassifier
from flair.data import Sentence
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import numpy as np
import requests


def grab_name(ticker):
    """grabs the full name of a company according to yahoo finance, given its ticker symbol"""

    stock = yf.Ticker(ticker)
    company_name = stock.info['longName']

    return company_name

# print(grab_name("AMZN"))





def grab_trending_tickers():
    """grabs the tickers of the companies with trending stocks and returns list of them"""

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

    exclude = ['S&P 500', 'Dow Jones Industrial Average','NASDAQ Composite','Russell 2000', 'NASDAQ','^']

    trending_tickers = []
    for item in data:
        ticker = yf.Ticker(item[0]).info['symbol']
        if ticker not in exclude:
            if "^" not in ticker:
                trending_tickers.append(ticker)
    
    return trending_tickers



def target_stocks(main_tickers):
    """ returns a dictionary of trending stock tickers and inputted tickers 
    with keys "trending" and "main" respectively"""

    
    # names of trending stocks
    trending = grab_trending_tickers()

    # dictionary with both sets of tickers
    stocktickers_dic = {"main":main_tickers}
    stocktickers_dic["trending"] = trending

    # print(stocks)
    return stocktickers_dic


def get_articles(company):
    """uses NewsAPI to return a list of all the Yahoo Entertainment news articles with a company
    name as a keyword given certain parameters, in order of relevancy"""
           
    newsapi = NewsApiClient(api_key='f533c47222e44b40a1ae23d73bf08d86')

    all_articles = newsapi.get_everything(q=company, from_param="2023-03-28",
        to="2023-04-27",
        language="en",
        sort_by="relevancy",
        page=1)   

    # print(type(all_articles['articles']))

    articles = []

    for article in all_articles['articles']:
        if article['source']['name'] == 'Yahoo Entertainment':
            articles.append(article)

    return articles


   
def get_content(article):
    """return the content of an article for use with flair sentiment analysis
    select only the first {max_words} words and ommit certain words, input is 
    article in dictionary format from news api"""
    
    max_words = 25
    unwanted_words = ["HOME", "MAIL", "NEWS", "FINANCE", "SPORTS", "ENTERTAINMENT", "LIFE", "SEARCH", "SHOPPING", "YAHOO", "PLUS", "MORE..."]

    # Get the full text of the article using its URL
    response = requests.get(article['url'])
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text().strip().split()[:max_words]
    content = " ".join([word for word in content if word not in unwanted_words])
    # Replace all occurrences of two consecutive newline characters with one newline character
    content = content.replace("\n\n", "\n")
    # print(content)
    return content



# ____________________________________________________________________________confirm v
def get_sentiment(content):
    """analyse sentiment of an article's content using flair and return score
    in as a positive or negative value, input is article content"""

    classifier = TextClassifier.load('en-sentiment')

    # Analyze the sentiment of the article's content using Flair
    sentence = Sentence(content)
    classifier.predict(sentence)
    sentiment = sentence.labels[0].value
    score = sentence.labels[0].score

    # print(f'Sentiment: {sentiment}, Score: {score}')
    if sentiment == "POSITIVE":
        score = score
    else:
        score = -score
    return score 

# ____________________________________________________________________________confirm ^


def average_sentiment(articles):
    """returns an average sentiment rating for the {max_articles} most relevant articles
    uses the holdrange parameter to differentiate between hold/buy/sell
    input is articles as list"""

    print(len(articles))
    
    total_score = 0
    articlenumber = 0 #to count the number articles released
    max_articles = 5

    use = min(max_articles,len(articles))

    while articlenumber < use:
        content = get_content(articles[articlenumber])
        score = get_sentiment(content)
        total_score += score
        articlenumber += 1

    avg = total_score / max_articles

    holdrange = .25

    if avg < -holdrange:
        sentrating = "negative"
    elif avg > holdrange:
        sentrating = "positive"
    else:
        sentrating = "neutral"
    
    # print(f' This is the avg rating of the {avg}')
    # print (f' The sentiment analysis is: {sentrating}')

    return sentrating


def analyst_rating(ticker):
    """returns analyst stock rating from yahoo finance for a given ticker"""

    data = yf.Tickers(ticker)
    rate = (data.tickers[ticker].info['recommendationKey'])

    return rate




def combine_scoreandrating(analyst_rate,sent_rate):
    """returns our rating using inputted analyst rating (str) and sentiment score (str)"""


    if 'buy' in analyst_rate:
        if sent_rate == 'negative':
            result = 'Hold'
        else:
            result = 'Buy'
    elif 'sell' in analyst_rate:
        if sent_rate == 'positive':
            result = 'Hold'
        else: 
            result = 'Sell'
    else:
        if sent_rate == 'neutral':
            result = 'Hold'
        elif sent_rate == 'negative':
            result = 'Sell'
        else: 
            result = 'Buy'
    
    return result 


def market_mood(main_tickers):

    stocktickers_dic = target_stocks(main_tickers)
    stocknames_dic = {}
    print()

    for key in stocktickers_dic:
        for ticker in stocktickers_dic[key]:

            type_ = key
            company = grab_name(ticker)
            articles = get_articles(company)
            print(company)
            sent_rate = average_sentiment(articles)
            analyst_rate = analyst_rating(ticker)
            our_rate = combine_scoreandrating(analyst_rate,sent_rate)
    

            ticker_dic = {}
            ticker_dic["Type"] = type_
            ticker_dic["Ticker"] = ticker
            ticker_dic["Analyst Rating"] = analyst_rate
            ticker_dic["Sentiment Rating"] = sent_rate
            ticker_dic["MarketMood Rating"] = our_rate

            stocknames_dic[company] = ticker_dic

    return stocknames_dic



    


# print(f' After reading through all the articles the decision is that {ticker} shows rather {(average_sentiment(article_list(stocks)))} analysis.')
# print(f' The analyst says: {(analyst_rating (ticker))} ')
# print(f' We think that you should {our_result()} {ticker}.')



def main():
    print(grab_trending_tickers())
    mytickers = ["MSFT","AAPL","AMZN"]
    result = market_mood(mytickers)
    print(result)


    

if __name__ == "__main__":
    main()
