import sys
import requests
import re
from bs4 import BeautifulSoup


# Get page text

def getBody(url):

    agents = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response= requests.get(url, headers=agents,timeout=10)
        response.raise_for_status()

        soup =BeautifulSoup(response.text, "html.parser")

        if soup.body:
            text =soup.body.get_text()
        else:
            text= ""

        return text
    except Exception:
        print("Unable to fetch url")
        return  None

#Polynomial rolling hash 

def polynomial_hash(word):
    P =53
    MOD = 2**64

    hash_value= 0
    power =1

    for ch in word:
        ascii= ord(ch)

        hash_value=(hash_value + ascii* power) % MOD
        power=(power * P) % MOD

    return hash_value

#Count word frequency

def wordCount(text):
    text=text.lower()

    words= re.findall(r"[a-z0-9]+", text)

    frequency= {}

    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] =1

    return frequency

#Computing Simhash

def simHash(word_frequency):

    bit_vector =[0]*64

    

    for word in word_frequency:

        freq = word_frequency[word]
        word_hash = polynomial_hash(word)

        for i in range(64):

            # check if ith bit is 1
            if (word_hash >> i) & 1:
                bit_vector[i] += freq
            else:
                bit_vector[i] -= freq

    # build final hash
    final_hash= 0

    for i in range(64):
        if bit_vector[i] > 0:
            final_hash = final_hash | (1 << i)

    return final_hash

#Compare two simhashes

def commonBits(hash1, hash2):

    count = 0

    for i in range(64):
        bit1 = (hash1 >> i) & 1
        bit2 = (hash2 >> i) & 1

        if bit1 == bit2:
            count += 1

    return count

def main():

    if len(sys.argv) != 3:
        print("Invalid input type")
        sys.exit(1)

    url1 = sys.argv[1]
    url2 = sys.argv[2]

    try:
        print("Fetching  URLs")
        text1=getBody(url1)
        text2=getBody(url2)
        if not text1 or not text2:
            print("Unable to fetch page")
            return None
        print("Counting word frequency")
        freq1=wordCount(text1)
        freq2=wordCount(text2)

        print("Computing simhash")
        simhash1 = simHash(freq1)
        simhash2 = simHash(freq2)

        common =commonBits(simhash1, simhash2)

        print("Common bits in simhash:", common, "out of 64")

    except requests.exceptions.RequestException as e:
        print("Eror while fetching page:")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()