import requests
from bs4 import BeautifulSoup

def scrape_faq(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for potential FAQ containers
        faq_containers = soup.find_all(['section', 'div'], class_=lambda x: x and 'faq' in x.lower())
        
        if not faq_containers:  # Additional attempt if no direct 'faq' class is found
            faq_containers = soup.find_all(['h2', 'h3', 'h4'], text=lambda x: x and 'faq' in x.lower())
        
        if not faq_containers:
            print("No FAQ section found.")
            return
        
        print("FAQ Section(s) Found:\n")
        for container in faq_containers:
            print(container.get_text(strip=True, separator="\n"))
            print("\n" + "-" * 50 + "\n")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
url = input("Enter the website URL to scrape FAQ: ").strip()
scrape_faq(url)
