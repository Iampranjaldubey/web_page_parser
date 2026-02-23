import sys
import requests
import re
from bs4 import BeautifulSoup

# p = 53
P = 53

# m = 2^64
MOD = 2 ** 64

# Get page text

def get_body_text(url):

    agents= {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=agents)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.body:
        text = soup.body.get_text()
    else:
        text = ""

    return text

#Count word frequency

def count_words(text):

    # convert to lowercase
    text = text.lower()

    # find all words (alphanumeric only)

    words = re.findall(r"[a-z0-9]+", text)

    frequency = {}

    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency

#Polynomial rolling hash (64 bit)

def polynomial_hash(word):

    hash_value = 0
    power = 1

    for ch in word:
        ascii_value = ord(ch)

        hash_value = (hash_value + ascii_value * power) % MOD
        power = (power * P) % MOD

    return hash_value

#Compute Simhash

def compute_simhash(word_frequency):

    # create list of 64 zeros
    bit_vector = []

    for i in range(64):
        bit_vector.append(0)

    # process each word
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
    final_hash = 0

    for i in range(64):
        if bit_vector[i] > 0:
            final_hash = final_hash | (1 << i)

    return final_hash

#Compare two simhashes

def count_common_bits(hash1, hash2):

    count = 0

    for i in range(64):

        bit1 = (hash1 >> i) & 1
        bit2 = (hash2 >> i) & 1

        if bit1 == bit2:
            count += 1

    return count

# Main Program

def main():

    if len(sys.argv) != 3:
        print("Usage: python main.py <URL1> <URL2>")
        sys.exit(1)

    url1 = sys.argv[1]
    url2 = sys.argv[2]

    try:
        print("Fetching first URL...")
        text1 = get_body_text(url1)
        print(text1[:500])

        print("Fetching second URL...")
        text2 = get_body_text(url2)
        print(text2[:500])

        print("Counting word frequency...")
        freq1 = count_words(text1)
        freq2 = count_words(text2)

        print("Computing simhash...")
        simhash1 = compute_simhash(freq1)
        simhash2 = compute_simhash(freq2)

        common = count_common_bits(simhash1, simhash2)

        print("Common bits in simhash:", common, "out of 64")

    except requests.exceptions.RequestException as e:
        print("Error while fetching page:")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()