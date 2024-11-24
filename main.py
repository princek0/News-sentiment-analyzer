import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup

# Yahoo finance headlien scraper

url= input("Enter Yahoo finance URL:")
page = requests.get(url)
soup = BeautifulSoup(page.text, features="html.parser")
h1 = soup.find('h1', class_='cover-title')
h1_text = h1.get_text(strip=True) 

# NLTK sentiment analyzer

sia = SentimentIntensityAnalyzer() # Initialise sentiment analyzer

# sentiment lexicon
nltk.download('vader_lexicon') # a pretrained sentiment lexicon
financial_lexicon = { # custom lexicon for financial extension
    "bullish": 3.0,
    "rally": 2.5,
    "outperform": 1.5,
    "strong": 1.0,
    "expansion": 2.0,
    "exceeded": 2.0,
    "launching": 1.5,
    "bearish": -3.0,
    "loss": -2.5,
    "profit warning": -3.5,
    "miss estimates": -2.5,
    "underperform": -2.0,
    "weak": -3.0,
    "selloff": -2.5,
    "layoff": -1.5,
    "default": -3.0,
    "acquisition": 2.5,
    "merger": 1.5,
    "dividend": 1.0,
    "downgrade": -2.5,
    "upgrade": 2.5,
    "maintain": 0.0,
    "recession": -2.5,
    "inflation": -1.5,
    "steady": 0.5,
    "stable": 0.5,
}

sia.lexicon.update(financial_lexicon) # updating pretrained lexicon





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