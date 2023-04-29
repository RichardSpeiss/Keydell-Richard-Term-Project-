from newsapi.newsapi_client import NewsApiClient
import requests
from bs4 import BeautifulSoup
from flair.models import TextClassifier
from flair.data import Sentence

# Initiate NewsApiClient with your API key
newsapi = NewsApiClient(api_key="f533c47222e44b40a1ae23d73bf08d86")

# Initialize the Flair sentiment classifier
classifier = TextClassifier.load("en-sentiment")

# Define the keyword you want to search for
keyword = "SIVB"

# Get the 5 most recent articles that contain the keyword
articles = newsapi.get_everything(
    q=keyword,
    from_param="2023-03-18",
    to="2023-04-17",
    language="en",
    sort_by="relevancy",
    page=1,
)

articlenumber = 0  # to count the number articles released
total = 0
max_articles = 5
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


# Loop through each article and print the body text
for article in articles["articles"]:
    if article["source"]["name"] == "Yahoo Entertainment":
        articlenumber += 1
        # Check if we have reached the maximum number of articles
        if articlenumber > max_articles:
            break
        print(articlenumber)
        print("\n")
        print(f" The following article is from {article['source']['name']}")
        print(f" The following article was released at {article['publishedAt']}")
        print(article["title"])
        print(article["url"])
        print("\n")

        # Get the full text of the article using its URL
        response = requests.get(article["url"])
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.get_text().strip().split()[:max_words]
        content = " ".join([word for word in content if word not in unwanted_words])
        # Replace all occurrences of two consecutive newline characters with one newline character
        content = content.replace("\n\n", "\n")
        print(content)

        # #Find the HTML element that contains the main text of the article
        # main_text = soup.find('div', class_='article-body')

        # #Extract the text from the main text element and print it
        # paragraphs = main_text.find_all('p') if main_text else []
        # for paragraph in paragraphs:
        #     print

        # Analyze the sentiment of the article's content using Flair
        sentence = Sentence(content)
        classifier.predict(sentence)
        sentiment = sentence.labels[0].value
        score = sentence.labels[0].score

        print(f"Sentiment: {sentiment}, Score: {score}")

        print("\n")

        total = articlenumber
        print(total)
