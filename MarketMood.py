from newsapi.newsapi_client import NewsApiClient
from flair.models import TextClassifier
from flair.data import Sentence
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

import requests
import datetime
import csv
import os


def grab_name(ticker: str) -> str:
    """returns the full string name of a company according to yahoo finance, given its ticker symbol"""
    stock = yf.Ticker(ticker)
    company_name = stock.info["longName"]
    return company_name


# print(grab_name("AMZN"))


def get_previous_close(ticker: str) -> float:
    """returns the previous closing price for the stock using y.finance, given ticker"""
    stock = yf.Ticker(ticker)
    price = stock.history(period="5d").Close.backfill().iloc[-1]
    return price


def grab_trending_tickers() -> list:
    """grabs the tickers of the companies with trending stocks and returns list of them"""

    url = "https://finance.yahoo.com/trending-tickers"

    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    headers = [th.text for th in table.find("thead").find_all("th")]

    data = []
    for tr in table.find("tbody").find_all("tr"):
        tds = tr.find_all("td")
        stock_data = [td.text.strip() for td in tds]
        stock_data.pop(-2)
        stock_data.pop(-2)
        data.append(stock_data)
    # print(data)

    exclude = [
        "S&P 500",
        "Dow Jones Industrial Average",
        "NASDAQ Composite",
        "Russell 2000",
        "NASDAQ",
        "^",
        "entitySlug",
        "N/A",
    ]

    trending_tickers = []
    for entry in data:
        match = 0
        # print(entry)
        for object in entry:
            for item in exclude:
                if item in object:
                    match = 1
        if match == 0:
            ticker = yf.Ticker(entry[0]).info["symbol"]
            trending_tickers.append(ticker)

    return trending_tickers


def target_stocks(query_tickers: str) -> dict:
    """returns a dictionary of trending stock tickers and inputted tickers
    with keys "trending" and "main" respectively"""

    trending = grab_trending_tickers()

    stocktickers_dic = {"query": query_tickers}
    stocktickers_dic["trending"] = trending

    # print(stocks)
    return stocktickers_dic


def get_articles(company: str) -> list:
    """uses NewsAPI to return a list of all the Yahoo Entertainment news articles with a company
    name as a keyword given certain parameters, in order of relevancy. Each article is a dict"""

    newsapi = NewsApiClient(api_key="f533c47222e44b40a1ae23d73bf08d86")

    today = datetime.date.today()
    start = today - datetime.timedelta(days=25)

    all_articles = newsapi.get_everything(
        q=company,
        from_param=start,
        to=today,
        language="en",
        sort_by="relevancy",
        page=1,
    )
    # print(type(all_articles['articles']))

    articles = []
    for article in all_articles["articles"]:
        if article["source"]["name"] == "Yahoo Entertainment":
            articles.append(article)

    return articles


def get_content(article: dict) -> str:
    """return the content of an article for use with flair sentiment analysis
    select only the first {max_words} words and ommit certain words, input is
    article in dictionary format from news api"""

    max_words = 25
    unwanted_words = [
        "HOME",
        "MAIL",
        "NEWS",
        "FINANCE",
        "SPORTS",
        "ENTERTAINMENT",
        "LIFE",
        "SEARCH",
        "SHOPPING",
        "YAHOO",
        "PLUS",
        "MORE...",
    ]

    response = requests.get(article["url"])
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text().strip().split()[:max_words]
    content = " ".join([word for word in content if word not in unwanted_words])
    content = content.replace("\n\n", "\n")
    # print(type(content))
    return content


def get_sentiment(content: str) -> float:
    """analyse sentiment of an article's content using flair and return score
    in as a positive or negative value, input is article content"""

    classifier = TextClassifier.load("en-sentiment")
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


def average_sentiment(articles: list) -> str:
    """returns an average sentiment rating for the {max_articles} most relevant articles
    uses the holdrange parameter to differentiate between hold/buy/sell
    input is articles as list"""

    # print(len(articles))
    total_score = 0
    articlenumber = 0  # to count the number articles released
    max_articles = 5
    use = min(max_articles, len(articles))

    while articlenumber < use:
        content = get_content(articles[articlenumber])
        score = get_sentiment(content)
        total_score += score
        articlenumber += 1

    avg = total_score / max_articles
    holdrange = 0.25
    if avg < -holdrange:
        sentrating = "negative"
    elif avg > holdrange:
        sentrating = "positive"
    else:
        sentrating = "neutral"

    # print(f' This is the avg rating of the {avg}')
    # print (f' The sentiment analysis is: {sentrating}')

    return sentrating


def analyst_rating(ticker: str) -> str:
    """returns analyst stock rating from yahoo finance for a given ticker"""

    data = yf.Tickers(ticker)
    if "recommendationKey" in data.tickers[ticker].info:
        rate = data.tickers[ticker].info["recommendationKey"]
    else:
        rate = "none"

    return rate


def combine_scoreandrating(analyst_rate: str, sent_rate: str) -> str:
    """returns our rating using inputted analyst rating (str) and sentiment score (str)"""

    if "buy" in analyst_rate or "out" in analyst_rate:
        if sent_rate == "negative":
            result = "Hold"
        else:
            result = "Buy"
    elif "sell" in analyst_rate or "under" in analyst_rate:
        if sent_rate == "positive":
            result = "Hold"
        else:
            result = "Sell"
    else:
        if sent_rate == "neutral":
            result = "Hold"
        elif sent_rate == "negative":
            result = "Sell"
        else:
            result = "Buy"

    return result


def market_mood(query_tickers: list) -> dict:
    """given list of tickers, returns dictionary of given stocks and yahoo trending stocks
    with key as company name (from grab_name()), then sub dictionaries with 'Type' (main or trending),
    'Ticker', 'Analyst Rating' (from analyst_rating), 'Sentiment Rating' (from average_sentiment),
    and 'MarketMood Rating' (from combine_scoreandrating)"""

    stocktickers_dic = target_stocks(query_tickers)
    stocknames_dic = {}

    for key in stocktickers_dic:
        for ticker in stocktickers_dic[key]:
            type_ = key
            # print(ticker)
            price = get_previous_close(ticker)
            company = grab_name(ticker)
            # print(company)
            articles = get_articles(company)
            sent_rate = average_sentiment(articles)
            # sent_rate = "positive" #swap this in if dont want to wair for flair
            analyst_rate = analyst_rating(ticker)
            our_rate = combine_scoreandrating(analyst_rate, sent_rate)

            ticker_dic = {}
            ticker_dic["Ticker"] = ticker
            ticker_dic["Previous Close"] = price
            ticker_dic["Type"] = type_
            ticker_dic["Analyst Rating"] = analyst_rate
            ticker_dic["Sentiment Rating"] = sent_rate
            ticker_dic["MarketMood Rating"] = our_rate

            stocknames_dic[company] = ticker_dic

    return stocknames_dic


# testing_dict = {'Microsoft Corporation': {'Ticker': 'MSFT','Type': 'main', 'Analyst Rating': 'buy', 'Sentiment Rating': 'negative', 'MarketMood Rating': 'Hold'}, 'Apple Inc.': {'Ticker': 'AAPL', 'Type': 'main', 'Analyst Rating': 'buy', 'Sentiment Rating': 'negative', 'MarketMood Rating': 'Hold'}, 'Amazon.com, Inc.': {'Ticker': 'AMZN', 'Type': 'main', 'Analyst Rating': 'buy', 'Sentiment Rating': 'negative', 'MarketMood Rating': 'Hold'}}


def create_CSV(stocknames_dic: dict) -> None:
    """add data in stocknames_dic from 'market_mood()' to a csv file in repository's
    data folder, replace current addition if code was already run on todays date"""

    date = datetime.date.today()

    path = f"data/MarketMood_Ratings_{date}.csv"

    if os.path.exists(path):
        os.remove(path)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        fields = (
            "Company Name",
            "Ticker",
            "Previous Close",
            "Type",
            "Analyst Rating",
            "Sentiment Rating",
            "MarketMood Rating",
        )
        writer.writerow(fields)

        for key in stocknames_dic:
            writer.writerow([key] + list(stocknames_dic.get(key).values()))


def main():

    # input any stock tickers you wish to get a rating for
    mytickers = ["JXN", "AAL", "LULU"]

    result = market_mood(mytickers)
    print()
    print()
    print()
    print(result)
    print()
    print()
    print()
    create_CSV(result)
    print("All Done :)")


if __name__ == "__main__":
    main()
