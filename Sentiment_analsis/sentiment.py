
from newsapi import NewsApiClient
import requests
from bs4 import BeautifulSoup

# Initiate NewsApiClient with your API key
newsapi = NewsApiClient(api_key='f533c47222e44b40a1ae23d73bf08d86')

# Define the keyword you want to search for
keyword = 'Infosys'

# Get the 5 most recent articles that contain the keyword
articles = newsapi.get_everything(q=keyword, language='en', sort_by='publishedAt', page_size=5)

articlenumber = 0 #to count the number articles released
total = 0
# Loop through each article and print the body text
for article in articles['articles']:
    #if article['source']['name'] == 'Yahoo Entertainment' or article['source']['name'] == 'Motley Fool' or article['source']['name'] == 'PRNewswire' or article['source']['name'] == 'Biztoc.com'  or article['source']['name'] == 'TechCrunch' or article['source']['name'] == 'GlobeNewswire' or article['source']['name'] == 'MarketWatch' : # Check if the article is from specified sources
        articlenumber += 1

        print(articlenumber)
        print('\n')
        print(f" The following article is from {article['source']['name']}")
        print(f" The following article was released at {article['publishedAt']}")
        print(article['title'])
        print('\n')
        #print(article)

        # Get the full text of the article using its URL

        # #non parsed text
        # response = requests.get(article['url'])
        # content = response.text
        # print(content)


        # the parsed text 
        response = requests.get(article['url'])
        # soup = BeautifulSoup(response.content)    
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text().strip()
        print(content)

        # Find the HTML element that contains the main text of the article
        main_text = soup.find_all('div','p')  # Change 'article-body' to the class or ID of the main text element on the website

        # # Extract the text from the main text element and print it
        # if main_text:
        #     # get all the paragraphs of the article
        #     paragraphs = main_text.find_all('div','p')
        #     for paragraph in paragraphs:
        #         print(paragraph.text)
        # else:
        #     print('No more article text found')
    
        print('\n')
    
        total = articlenumber
        print(total)


import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize    



def removestops():

    text = articles
    text_tokens = word_tokenize(text)

    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

    return(tokens_without_sw)


'''
The following code came from ChatGPT after asking it to give me 
a random piece of code to add to my orginal code in order to furthur 
analyze the text 


'''
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def analyze_sentiment():
    sia = SentimentIntensityAnalyzer()
    text = ''
    for article in articles['articles']:
        response = requests.get(article['url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text().strip()
        text += content
    sentiment_scores = sia.polarity_scores(text)
    return sentiment_scores


def main():

    # print()
    # print()
    # print("Histogram starts below ")
    # print()
    # print(process_site())
    # print()
    # print()
    # print("Shortened Text Below")
    # print()
    # print(removestops())
    print()
    print()
    print("Sentiment Analysis Results:")
    print()
    print(analyze_sentiment())




if __name__ == '__main__':
    main()
