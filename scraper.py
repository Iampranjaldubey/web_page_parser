import sys
import requests
from bs4 import BeautifulSoup

def isValid(url):
    if not url.startswith(("https://", "http://")):
        # print("invalid url")

        return None
    return url

def fetchPage(url):
    agents={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
        }
    response=requests.get(url,headers=agents,timeout=10)
    response.raise_for_status()
    return response

def main():

    if len(sys.argv)< 2:

        print("No URL provided")

        sys.exit(1)

    url =isValid(sys.argv[1])
    if not url:

        print("Invalid URL")

        sys.exit(1)

    try:
        print("Feching page\n")
        response=fetchPage(url)
        print("fetched the page")

        soup= BeautifulSoup(response.text, "html.parser")
        
        print("\n__PAGE TITLE__")

        if soup.title:
            title=soup.title.get_text().strip()
            print(title)
        else:
            print("No title found")

        print("\n__PAGE BODY__")

        body = soup.body
        if body:
            # removing HTML tags
            bodyText= body.get_text(separator="\n", strip=True)
            print(bodyText)
        else:
            print("No body found")
        
        print("\n__ALL LINKS__")

        links = set() 
        for link in soup.find_all("a"):
            href=link.get("href")
            if href:
                links.add(href)

        if links:
            for link in links:
                print(link)
        else:
            print("No links found")

    except requests.exceptions.RequestException as e:
        print("Error")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()