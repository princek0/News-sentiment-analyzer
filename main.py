import requests
import beautifulsoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)