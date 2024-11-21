import requests
import bs4

URL = "https://www.thisisprince.com/"
page = requests.get(URL)

print(page.text)