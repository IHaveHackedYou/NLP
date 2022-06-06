from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import json
import numpy as np

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class NumCounterNew:
    def __init__(self):
        pass

    # get soup required by BeautifulSoup
    def get_soup_by_url(self, url):
        result = requests.get(url)
        html_file = result.text 
        return BeautifulSoup(html_file, "html.parser")

    def import_file_as_dictionary(self, filename):
      os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")

      with open(filename, 'r') as f:
        data = json.load(f)
      return data

    def store_file_as_json(self, filename, data):
      with open(filename, 'w') as f:
        json.dump(data, f)
    
    def load_file(self, filename):
      os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
      data = pd.read_csv(filename)
      words = data["words"].values.tolist()
      counts = data["counts"].values.tolist()
      # counts = np.ones(len(words))
      dict_ = dict(zip(words, counts))
      return dict_
    
    def save_file(self, filename, data):
      words = list(data.keys())
      counts = list(data.values())
      df = pd.DataFrame({"words": words, "counts": counts})
      df.sort_values(by=["counts"], ascending=False, inplace=True)
      df.to_csv(filename)

    def get_all_text(self, url):
      soup = self.get_soup_by_url(url)
      text = soup.get_text()
      text = text.lower()
      text = text.translate ({ord(c): " " for c in '!@#$%^&*()[]{};:,./<>?\|`~-=_+\©"“'})
      text = text.split()
      return text

    def add_text_to_counts(self, load_filename, save_filename, text):
      dict_ = self.load_file(load_filename)
      for word in text:
        if len(word) <= 1:
          continue
        word = word.strip()
        if word in dict_:
          dict_[word] += 1
      self.save_file(save_filename, dict_)
    
    def add_list_to_counts(self, load_filename, save_filename, list, iterations_to_save=100):
      dict_ = self.load_file(load_filename)
      i = 0
      for url in list:
        print(url)
        text = self.get_all_text(url)
        i += 1
        for word in text:
          if len(word) <= 1:
            continue
          word = word.strip()
          if word in dict_:
            dict_[word] += 1
        if i % iterations_to_save == 0:
          self.save_file(save_filename, dict_)

    def create_gutenberg_urls(self, num_books, start_index):
        urls = []
        for i in range(num_books):
            urls.append(f"https://www.gutenberg.org/cache/epub/{i+start_index}/pg{i+start_index}.txt")
        return urls

new_counter = NumCounterNew()
# to 10600
# urls = new_counter.create_gutenberg_urls(10000, 18000)
urls = ["https://en.wikipedia.org/wiki/programming",
             "https://en.wikipedia.org/wiki/words",
             "https://en.wikipedia.org/wiki/history",
             "https://en.wikipedia.org/wiki/elephant",
             "https://en.wikipedia.org/wiki/giraffe",
             "https://en.wikipedia.org/wiki/train",
             "https://en.wikipedia.org/wiki/airplane",
             "https://en.wikipedia.org/wiki/school",
             "https://en.wikipedia.org/wiki/highschool",
             "https://en.wikipedia.org/wiki/midschool",
             "https://en.wikipedia.org/wiki/Human_history",
             "https://en.wikipedia.org/wiki/war",
             "https://en.wikipedia.org/wiki/europe",
             "https://en.wikipedia.org/wiki/glasgow",
             "https://en.wikipedia.org/wiki/washington",
             "https://en.wikipedia.org/wiki/manhattan",
             "https://en.wikipedia.org/wiki/flag",
             "https://en.wikipedia.org/wiki/nation",
             "https://en.wikipedia.org/wiki/sport",
             "https://en.wikipedia.org/wiki/world",
             "https://en.wikipedia.org/wiki/statue_of_liberty",
             "https://en.wikipedia.org/wiki/boeing",
             "https://en.wikipedia.org/wiki/reading",
             "https://en.wikipedia.org/wiki/life",
             "https://en.wikipedia.org/wiki/Dubai",
             "https://en.wikipedia.org/wiki/car",
             "https://en.wikipedia.org/wiki/biology",
             "https://en.wikipedia.org/wiki/philosphy",
             "https://en.wikipedia.org/wiki/usa",
             "https://en.wikipedia.org/wiki/germany",
             "https://en.wikipedia.org/wiki/english",
             "https://en.wikipedia.org/wiki/harry_potter",
             "https://en.wikipedia.org/wiki/james_bond",
             "https://en.wikipedia.org/wiki/food",
             "https://en.wikipedia.org/wiki/banana",
             "https://en.wikipedia.org/wiki/apple",
             "https://en.wikipedia.org/wiki/language",
             "https://en.wikipedia.org/wiki/ber",
             "https://en.wikipedia.org/wiki/english_wikipedia",
             "https://en.wikipedia.org/wiki/Online_encyclopedia",
             "https://en.wikipedia.org/wiki/British_English",
             "https://en.wikipedia.org/wiki/youtube",
             "https://en.wikipedia.org/wiki/facebook",
             "https://en.wikipedia.org/wiki/instagram",
             "https://en.wikipedia.org/wiki/tesla",
             "https://en.wikipedia.org/wiki/new_york",
             "https://en.wikipedia.org/wiki/Online_video_platform",
             "https://en.wikipedia.org/wiki/Entertainment",
             "https://en.wikipedia.org/wiki/Most_common_words_in_English",
             "https://en.wikipedia.org/wiki/Oxford_English_Corpus",
             "https://en.wikipedia.org/wiki/book",
             "https://en.wikipedia.org/wiki/elon_musk",
             "https://en.wikipedia.org/wiki/copyright",
             "https://en.wikipedia.org/wiki/drawing",
             "https://en.wikipedia.org/wiki/sketching",
             "https://en.wikipedia.org/wiki/dollar",
             "https://en.wikipedia.org/wiki/euro",
             "https://en.wikipedia.org/wiki/!",
             "https://en.wikipedia.org/wiki/?",
             "https://en.wikipedia.org/wiki/dot",
             "https://en.wikipedia.org/wiki/beer",
             "https://en.wikipedia.org/wiki/architecture",
             "https://en.wikipedia.org/wiki/text",
             "https://en.wikipedia.org/wiki/money",
             "https://en.wikipedia.org/wiki/paris",
             "https://en.wikipedia.org/wiki/hotel",
             "https://en.wikipedia.org/wiki/motel",
             "https://en.wikipedia.org/wiki/city",
             "https://en.wikipedia.org/wiki/internet",
             "https://en.wikipedia.org/wiki/influencer",
             "https://en.wikipedia.org/wiki/youth",
             "https://en.wikipedia.org/wiki/Languages_of_the_United_States",
             "https://en.wikipedia.org/wiki/unity",
             "https://en.wikipedia.org/wiki/bible",
             "https://en.wikipedia.org/wiki/church",
             "https://en.wikipedia.org/wiki/marvel",
             "https://en.wikipedia.org/wiki/movie",
             "https://en.wikipedia.org/wiki/superman",
             "https://en.wikipedia.org/wiki/batman",
             "https://en.wikipedia.org/wiki/fortnite",
             "https://en.wikipedia.org/wiki/slang",
             "https://en.wikipedia.org/wiki/drink",
             "https://en.wikipedia.org/wiki/queen",
             "https://en.wikipedia.org/wiki/king",
             "https://en.wikipedia.org/wiki/great_britian",
             "https://en.wikipedia.org/wiki/london",
             "https://en.wikipedia.org/wiki/atlantic_ocean",
             "https://en.wikipedia.org/wiki/ocean",
             "https://en.wikipedia.org/wiki/English_people",
             "https://en.wikipedia.org/wiki/football",
             "https://en.wikipedia.org/wiki/basketball",
             "https://en.wikipedia.org/wiki/australia",
             "https://en.wikipedia.org/wiki/england",
             "https://en.wikipedia.org/wiki/wales",
             "https://en.wikipedia.org/wiki/canada",
             "https://en.wikipedia.org/wiki/star_wars",
             ]
new_counter.add_list_to_counts("new_word_list.txt", "new_word_list.txt", urls, 200)
