import requests
from bs4 import BeautifulSoup

url='https://uk.finance.yahoo.com/news/mixing-it-up-porsche-unveils-a-new-gas-powered-911-carrera-t-and-electric-taycan-gts-160019197.html'
page = requests.get(url)
soup = BeautifulSoup(page.text, features="html.parser")
h1 = soup.find('h1', class_='cover-title')
h1_text = h1.get_text(strip=True) 

print(f"{h1_text}")