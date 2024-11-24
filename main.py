import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup

# Yahoo finance headlien scraper

url= input("Enter Yahoo finacne URL:")
page = requests.get(url)
soup = BeautifulSoup(page.text, features="html.parser")
h1 = soup.find('h1', class_='cover-title')
h1_text = h1.get_text(strip=True) 

# NLTK sentiment analyzer

nltk.download('vader_lexicon') # a pretrained sentiment analyzer
sia = SentimentIntensityAnalyzer() # Initialise sentiment analyzer

sentiment = sia.polarity_scores(h1_text) # analyzing sentiment
compound_score = sentiment['compound']

# setting up human readable categories based on the compound_score
if compound_score > 0.05:
    sentiment_category = 'positive'
elif compound_score < -0.05:
    sentiment_category = 'negative'
else:
    sentiment_category = 'neutral'

print(f"{h1_text}")
print(sentiment)
print(f"Headline sentiment: {sentiment_category}")