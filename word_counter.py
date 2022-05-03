from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class NumCounter:
    def __init__(self):
        pass

    def get_soup_by_url(self, url):
        result = requests.get(url)
        html_file = result.text 
        return BeautifulSoup(html_file, "html.parser")

    def get_all_text(self, url):
        soup = self.get_soup_by_url(url)
        text = soup.get_text()
        text = text.replace("\n", "")
        text = text.replace('"', "")
        text = text.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\©"""})
        new_text = text
        # for i in range(len(text)-1):
        #   if text[i].islower() and text[i+1].isupper():
        #     # new_text = new_text + text[i] + " "
        #     new_text = "".join([new_text, text[i], " "])
        #   else:
        #     # new_text = new_text + text[i]
        #     new_text = "".join([new_text, text[i]])

        new_text = new_text.replace("  ", " ")   
        new_text = new_text.lower()
        return new_text

    def add_plain_text_to_counts(self, text, words, counts):
        new_words = words
        new_counts = counts
        text_to_count = text.split()

        for word in text_to_count:
            if len(word) == 1 or any(x in word for x in DIGITS):
                continue
            if word not in words:
                new_words.append(word)
                new_counts.append(1)
            else:
                index = new_words.index(word)
                new_counts[index] += 1
        return new_words, new_counts


    def create_df(self, words, counts):
        df = pd.DataFrame(data={"counts": counts, "words": words})
        return df

    def create_gutenberg_urls(self, num_books, start_index):
        urls = []
        for i in range(num_books):
            urls.append(f"https://www.gutenberg.org/cache/epub/{i+start_index}/pg{i+start_index}.txt")
        return urls

    def remove_one_counts(self):
        if os.path.exists("word_frequency.txt"):
            df = pd.read_csv("word_frequency.txt")

        for index, row in df.iterrows():
            if row["counts"] == 1:
                df.drop(index, inplace=True)
                continue
        
        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        if os.path.exists("word_frequency.txt"):
            os.remove("word_frequency.txt")
        df.to_csv("word_frequency.txt")
        return df

    def iterate_through_urls(self, urls, filename):
        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            words = df["words"].values.tolist()
            counts = df["counts"].values.tolist()
        else:
            words = []
            counts = []

        for url in urls:
            print(url)
            text = self.get_all_text(url)
            words, counts = self.add_plain_text_to_counts(text, words, counts)
        df = self.create_df(words, counts)
        # df = self.remove_one_counts()
        df = df.sort_values(by="counts", ascending=False)

        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        if os.path.exists(filename):
            os.remove(filename)
        df.to_csv(filename)
        
        return df