from tokenize import String
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
# import re

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class NumCounter:
    def __init__(self):
        pass

    # get soup required by BeautifulSoup
    def get_soup_by_url(self, url):
        result = requests.get(url)
        html_file = result.text 
        return BeautifulSoup(html_file, "html.parser")

    
    # def get_all_text(self, url):
    #     soup = self.get_soup_by_url(url)
    #     text = soup.get_text()
    #     text = re.sub("[^a-zA ']", '', text)
    #     text = re.sub(r"\s+", " ", text)
    #     # for i in range(len(text)-1):
    #     #   if text[i].islower() and text[i+1].isupper():
    #     #     # new_text = new_text + text[i] + " "
    #     #     new_text = "".join([new_text, text[i], " "])
    #     #   else:
    #     #     # new_text = new_text + text[i]
    #     #     new_text = "".join([new_text, text[i]])
    #     text = text.lower()
    #     return text

    # get text by url
    def get_all_text_old(self, url):
        soup = self.get_soup_by_url(url)
        text = soup.get_text()
        text = text.lower()
        text = text.replace("\n", "")
        text = text.replace('"', "")
        text = text.replace("“", "")
        text = text.translate ({ord(c): " " for c in '!@#$%^&*()[]{};:,./<>?\|`~-=_+\©"'})

        text = text.replace("  ", " ")   
        return text


    def add_plain_text_to_counts(self, text, words, counts):
        new_words = words
        new_counts = counts
        # split text into single words
        text_to_count = text.split()

        for word in text_to_count:
            # if word consists of 1 char and is doesn't contain a digit
            if len(word) == 1 or word in DIGITS:
                continue

            if word not in words:
                new_words.append(word)
                new_counts.append(1)
            # if word is already in words
            else:
                index = new_words.index(word)
                new_counts[index] += 1
        return new_words, new_counts

    # create pandas dataframe
    # def create_df(self, words, counts):
    #     df = pd.DataFrame(data={"counts": counts, "words": words})
    #     return df

    def create_df(self, words, counts):
        df = pd.DataFrame(data={"counts": counts, "words": words})
        return df

    def create_df_with_trans(self, words, counts, translations):
        df = pd.DataFrame(data={"counts": counts, "words": words, "translations": translations})
        return df

    def create_gutenberg_urls(self, num_books, start_index):
        urls = []
        for i in range(num_books):
            urls.append(f"https://www.gutenberg.org/cache/epub/{i+start_index}/pg{i+start_index}.txt")
        return urls

    # remove words that occur less than x times
    def remove_one_counts(self, load_filename, store_filename, counts_to_remove=1):
        # get dataframe
        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        if os.path.exists(load_filename):
            df = pd.read_csv(load_filename)

        df = df.reset_index()

        # convert df to lists to safe performance
        counts = df["counts"].values.tolist()
        words = df["words"].values.tolist()

        for i in range(len(counts)):
            # if word occurs less than x times
            if counts[i] <= counts_to_remove:
                # save index of word
                counts_to_remove = i
                break
        
        # delete all "under" threshold where word/count occurs less than x times
        counts = counts [:counts_to_remove]
        words = words[:counts_to_remove]
        
        # save as df
        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        df = self.create_df(words, counts)
        df.to_csv(store_filename)
        return df

    def iterate_through_urls(self, urls, filename):
        # get df
        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            words = df["words"].values.tolist()
            counts = df["counts"].values.tolist()
        else:
            words = []
            counts = []
        i = 0
        # iterate through urls
        for url in urls:
            i+=1
            print(url)
            # get raw text
            text = self.get_all_text_old(url)
            # add text to words and counts
            words, counts = self.add_plain_text_to_counts(text, words, counts)
            # save every 50 words
            if i%50 == 0:
                df = self.create_df(words, counts)
                df = df.sort_values(by="counts", ascending=False)

                os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
                if os.path.exists(filename):
                    os.remove(filename)
                df.to_csv(filename)

        # save when done
        df = self.create_df(words, counts)
        df = df.sort_values(by="counts", ascending=False)

        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        if os.path.exists(filename):
            os.remove(filename)
        df.to_csv(filename)
        
        return df

    # normalize counts to numbers between 0 and 1
    def normalize_counts(self, load_filename, save_filename):
        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        if os.path.exists(load_filename):
            df = pd.read_csv(load_filename)

        df = df.reset_index()

        counts = df["counts"].values.tolist()
        words = df["words"].values.tolist()
        translations = df["translations"].values.tolist()
        
        max_num = counts[0]
        
        for i in range(len(counts)):
            counts[i] = counts[i] / max_num

        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        df = self.create_df(words, counts, translations)
        df.to_csv(save_filename)
        return df

    def remove_symbols_from_df(self, load_filename, store_filename, symbol, begin_end_symbol=None):
        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        if os.path.exists(load_filename):
            df = pd.read_csv(load_filename)

        df = df.reset_index()

        counts = df["counts"].values.tolist()
        words = df["words"].values.tolist()
        
        new_words = []
        new_counts = []

        for i in range(len(counts)):
            if str(words[i])[0] != begin_end_symbol and str(words[i])[-1] != begin_end_symbol and symbol not in str(words[i]):
                new_words.append(words[i])
                new_counts.append(counts[i])

        os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
        df = self.create_df(new_words, new_counts)
        df.to_csv(store_filename)
        return df