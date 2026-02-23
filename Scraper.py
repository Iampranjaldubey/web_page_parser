import sys
import requests
from bs4 import BeautifulSoup

def main():

    if len(sys.argv) < 2:

        print(" No URL provided.")

        sys.exit(1)

    url = sys.argv[1]

    if not url.startswith("http://") and not url.startswith("https://"):

        print("Invalid URL.")

        sys.exit(1)

    try:
        print("-Fetching data-")

        agents= {
        "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url,headers=agents)
        response.raise_for_status()

        print("Successfully fetched the page\n")

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract Page Title

        print("PAGE TITLE")

        if soup.title:
            print(soup.title.get_text().strip())
        else:
            print("No title found.")

        #  Extract Page Body Text
        print("\n PAGE BODY (TEXT ONLY) ")

        body = soup.body
        if body:
            # get_text removes all HTML tags automatically
            body_text = body.get_text(separator="\n", strip=True)
            print(body_text)
        else:
            print("No body content found.")

        # Extract All URLs
        
        print("\n ALL LINKS ")

        links = set()  # to avoid duplicates

        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                links.add(href)

        if links:
            for link in links:
                print(link)
        else:
            print("No links found.")

    except requests.exceptions.RequestException as e:
        print("Error while fetching the webpage:")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()