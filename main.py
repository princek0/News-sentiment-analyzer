import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from matplotlib import pyplot as plt

# Yahoo finance headline scraper
ticker = input("Enter stock ticker:")

# Setting up Selenium

chrome_options = Options()
chrome_options.add_argument("--headless") # Stops selenium from showing GUI

driver = webdriver.Chrome(options=chrome_options) 
driver.get( f"https://uk.finance.yahoo.com/quote/{ticker}/news/")

# Accepting permissions and cookies
try:
    cookie_button = driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]')
    cookie_button.click()
except Exception as e:
    print("No consent required:", e)

# Scrolling to avoid lazy loading
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Letting the automation pause for relevant elements to load successfully
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "clamp"))
)

# Obtaining headlines
page = driver.page_source
soup = BeautifulSoup(page, features="html.parser")
headlines = soup.find_all('h3', class_="clamp")  
headlines_text = [tag.get_text(strip=True) for tag in headlines]
driver.quit()

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
    "unveils": 1.0,
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
sentiments = [sia.polarity_scores(headline) for headline in headlines_text] # analyzing sentiment
compound_scores = [sia.polarity_scores(headline)['compound'] for headline in headlines_text] # list of compound scores in chronological order

# Plotting the compound_scores
x = [i for i in range(len(compound_scores))]

plt.plot(x, compound_scores, marker='o', linestyle='-', color='b')
plt.axhline(0, color='black',linewidth=1)
plt.axvline(0, color='black',linewidth=1)
plt.xticks(x)
plt.title(f"Compound sentiment scores of recent Yahoo finance articles on {ticker}")
plt.xlabel("Article index")
plt.ylabel("Compound Sentiment Score")
plt.grid(True)

plt.show()
