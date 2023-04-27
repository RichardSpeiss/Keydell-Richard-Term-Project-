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


# Define the keyword you want to search for
ticker = "TSLA"
stocks = target_stocks(ticker)
print()
print()
print()
print()

for key in stocks:
    print(key)
    print()
    print(stocks.get(key))
    print("----")
    print()



from newsapi.newsapi_client import NewsApiClient
import requests
from bs4 import BeautifulSoup
from flair.models import TextClassifier
from flair.data import Sentence

# Initiate NewsApiClient with your API key
newsapi = NewsApiClient(api_key='f533c47222e44b40a1ae23d73bf08d86')

# Initialize the Flair sentiment classifier
classifier = TextClassifier.load('en-sentiment')

# Define the keyword you want to search for


# Get the 5 most recent articles that contain the keyword
articles = newsapi.get_everything(q=stocks.get('main'), from_param="2023-03-27",
        to="2023-04-27",
        language="en",
        sort_by="relevancy",
        page=1)   

articlenumber = 0 #to count the number articles released
total = 0
max_articles = 5
max_words = 25
unwanted_words = ["HOME", "MAIL", "NEWS", "FINANCE", "SPORTS", "ENTERTAINMENT", "LIFE", "SEARCH", "SHOPPING", "YAHOO", "PLUS", "MORE..."]

article_list = []

# Loop through each article and print the body text
for article in articles['articles']:
    if article['source']['name'] == 'Yahoo Entertainment':
        articlenumber += 1
        # Check if we have reached the maximum number of articles
        if articlenumber > max_articles:
            break
        print(articlenumber)
        print('\n')
        print(f" The following article is from {article['source']['name']}")
        print(f" The following article was released at {article['publishedAt']}")
        print(article['title'])
        print(article['url'])
        print('\n')

        # Get the full text of the article using its URL
        response = requests.get(article['url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text().strip().split()[:max_words]
        content = " ".join([word for word in content if word not in unwanted_words])
        # Replace all occurrences of two consecutive newline characters with one newline character
        content = content.replace("\n\n", "\n")
        print(content)

        # Analyze the sentiment of the article's content using Flair
        sentence = Sentence(content)
        classifier.predict(sentence)
        sentiment = sentence.labels[0].value
        score = sentence.labels[0].score

        print(f'Sentiment: {sentiment}, Score: {score}')

        article_dict = {}
        #article_dict['source'] = article['source']['name']
        article_dict['publishedAt'] = article['publishedAt']
        #article_dict['title'] = article['title']
        article_dict['Sentiment'] = sentiment
        article_dict['Score'] = score
        #article_dict['url'] = article['url']
        #article_dict['content'] = content

        article_list.append(article_dict)
        article_list.sort(key=lambda x: x['publishedAt'], reverse=True)
        
       

        print('\n')
    
        total = articlenumber
        print(total)








    #math starts here 

avg = 0 
ratingtotal = 0 


for item in article_list:
    if item.get('Sentiment') == "POSITIVE":
        ratingtotal = ratingtotal + item.get('Score')
    elif item.get('Sentiment') == "NEGATIVE":
        ratingtotal = ratingtotal - item.get('Score')
    else:
        print("Cant addd this becasue error")

    #print (ratingtotal)
    avg = ratingtotal / 5

holdrange = .25
sentrating = ""

if holdrange <= avg >= -holdrange:
    sentrating = "neutral"

if avg < -holdrange:
    sentrating = "negative"

if avg > holdrange:
    sentrating = "positive"


print(f' This is the avg rating of the {avg}')

print (f' The sentiment analysis is: {sentrating}')


import pandas as pd
import yfinance as yf
import numpy as np
import time
import yfinance as yf

# List of stock tickers
tickers = ['AAPL', 'GOOG', 'TSLA']

# Fetch data for multiple tickers
data = yf.Tickers(tickers)

# Access data for each ticker
for ticker in tickers:
    print(ticker, data.tickers[ticker].info['recommendationKey'])


#print(article_list)



