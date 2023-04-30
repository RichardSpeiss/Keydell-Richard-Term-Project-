# Keydell-Richard-Term-Project-

Keydell Fuller and Richard Speiss
Spring 2023


### Purpose:

Our project is focused on using y.finance and flair sentiment analysis to create trade recommendations for given stocks, as well as those trending on yahoo finance. We hope to streamline the investing process for those new to stock market investing and help them progess more quickly to more advanced trading strategies. While our product does provide trade recomendations, we urge users to be cautious and use their own judgement when trading stocks. We are not liable for any financial consequences resulting from the use of our product. 

### Technologies
Our script primarily uses y.finance, flair, and News API. y.finance is an open source library that allows its users to access stock data from yahoo fiance. Flair is an articifial inteligence based sentiment analysis tool. News API returns JSON formatted news articles relating to a specified keyword using a specified timeframe, source, and organization type. In addition to these modules, our product imports pandas, rquests, datetime, csv, and os.  


### Code
Our script defines and calls over 10 functions to produce output. The market_mood() function is the structure of our code. The input is a list of query ticker symbols, and the output is a dictionary of dictionaries. The primary keys of the dictionary are full company names for each inputted stock. The [trending](https://finance.yahoo.com/trending-tickers) yahoo finance stocks are also included. The value of each company key is its own dictionary. The secondary keys are Ticker, Previous Close, Type, Analyst Rating, Sentiment Rating, and MarketMood Rating. The dictionary then passes through the crete_csv() function which creates a csv of the data in the clonned repositories data folder. Running the code will rewrite an existing file from the same day, as the date is included in the file name. 

####    **Ticker**
        Tickers part of the initial query list are listed as such. The grab_trending_tickers() function returns the tickers of the trending stocks on yahoo finance using y.finance. This function is embeded in the target_stocks() function, which is part of market_mood(). 

####    **Previous Close**
        The previous closeing price from the most recent trading day for each ticker is returned by get_previous_close(). 

####    **Type**
        Each ticker is has type query or trending. Query tickers are those inputted into market_mood(), and trending tickers are those from the yahoo finance trending stocks page.

####    **Analyst Rating**
        The Analyst rating for each ticker is returned by analyst_rating() using y.finance. There are five common ratings: Strong Buy, Buy, Hold, Sell, and Strong Sell. 

####    **Sentiment Rating** 
        The Sentiment rating of each ticker is returned by average_sentiment(). The flair sentiment analysis is initiated by the get_articles() function, which uses News API to return a list of recent news Yahoo Entertainment articles with the company name as a keyword. The average_sentiment() function encases the get_content() and get_sentiment() function. The get_content() function cycles through the list and returns a string of the first 25 words for each article. The get_sentiment() function retuns the positive or negative flair sentiment value. The average_sentiment() function completes the sentiment analysis process by averaging the values of the five most relevant articles, and produces a 'negative', 'neutral', or 'positive' sentiment rating. 

####    **MarketMood Rating**
        The MarketMood Rating is produced by the combine_scoreandrating() function. It uses the Analyst Rating and Sentiment Rating to produce the MarketMood Rating. It uses the following rules to produce its output. 

######  Analyst Sell or Strong Sell Rating with a
            Sentiment Positive Rating produces → Hold
            Sentiment Neutral Rating produces → Sell
            Sentiment Negative Rating produces → Sell
        
######  Analyst Hold Rating with a
            Sentiment Positive Rating produces → Buy
            Sentiment Neutral Rating produces → Hold
            Sentiment Negative Rating produces → Sell

######  Analyst Buy or Strong Buy Rating with a
            Sentiment Positive Rating produces → Buy
            Sentiment Neutral Rating produces → Buy
            Sentiment Negative Rating produces → Hold

### Rational

####    **Analyst Sell or Strong Sell Rating with a**

            **Sentiment Positive Rating produces → Hold**
            The positive rating gives evidence of possible price increases

            **Sentiment Neutral Rating produces → Sell**
            No additional value from sentiment analysis 

            **Sentiment Negative Rating produces → Sell**
            The negative rating enforces the Analyst decision 

        
####    **Analyst Hold Rating with a**

            **Sentiment Positive Rating produces → Buy**
            The positive rating gives evidence of possible price increases

            **Sentiment Neutral Rating produces → Hold**
            No additional value from sentiment analysis 

            **Sentiment Negative Rating produces → Sell**
            The negative rating gives evidence of possible price decreases 


####    **Analyst Buy or Strong Buy Rating with a**

            **Sentiment Positive Rating produces → Buy**
            The positive rating enforces the Analyst decision 

            **Sentiment Neutral Rating produces → Buy**
            No additional value from sentiment analysis 

            **Sentiment Negative Rating produces → Hold**
            The negative rating gives evidence of possible price decreases 


### Directions
To use this code, fist clone this repository on your computer. Input any stock tickers you wish to get a rating for in the mytickers[] list. After running the code, the CSV file will be created in the data folder of the repository with the date. Running the code after previously running it the same day will rewrite the CSV file. 