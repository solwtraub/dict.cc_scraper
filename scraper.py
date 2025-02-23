import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import os
import random

class Word:
    def __init__(self, word, gender, digits, use_cases):
        self.word = word
        self.gender = gender
        self.digits = digits
        self.use_cases = use_cases
    
    def __str__(self):
        return self.word
    

def translate_dictionary(path, num_words, seed):
    rng = np.random.default_rng(seed=seed)
    translated = []
    with open(path, "r") as file:
        words = file.read()
        rints = rng.integers(low=0, high=len(words), size=num_words)
        translated = [get_translation(words[i]) for i in rints]
    return translated


    
def get_translation(word):
    url = f"https://www.dict.cc/?s={word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Error: Unable to fetch data"

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract translations (they appear in table rows)
    translations = []
    for row in soup.select("tr[id^='tr']"):  # Target translation rows
        columns = row.find_all("td", class_="td7nl")  # Translations
        if len(columns) == 2:
            english, *rest = detect_word_patterns(strip_html(str(columns[0])))
            german, *rest = detect_word_patterns(strip_html(str(columns[1])))
            english = remove_leading_digits(english)
            german = remove_leading_digits(german)
            translations.append((german, english))

    return translations
def remove_leading_digits(text):
    # Regex to remove digits only when they appear in front of a word
    btext = re.sub(r"\d+$", '', text)
    return re.sub(r'^\d+(?=\w)', '', btext)

def detect_word_patterns(text):
    pattern = r"(?P<word>\w+)(?P<digits>\d+)?(?P<gender>\{[mfpl]+\})?(?P<use_cases>\[[^\]]*\])?"

    # Apply regex pattern
    match = re.search(pattern, text)

    if match:
        # Extract each group
        word = match.group('word')
        gender = match.group('gender') if match.group('gender') else None
        use_cases = match.group('use_cases') if match.group('use_cases') else None
        return word, gender, use_cases
    return None
def strip_html(string):
    return re.sub(r"<.*?>", "", string)
# 🔥 Example Usage
print(os.getcwd())
rng = np.random.default_rng()
translated = translate_dictionary("wordlist-german.txt", 10, random.randint(1, 100))
for i in translated:
    print(i)