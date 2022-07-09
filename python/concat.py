import os
import pandas as pd

store_file_name = "translations.txt"

def create_df(words, counts, translations):
  df = pd.DataFrame(data={"counts": counts, "words": words, "translations": translations})
  return df

os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
if os.path.exists(store_file_name):
  df = pd.read_csv(store_file_name)
  translations = df["translations"].values.tolist()

filename = "word_frequency_no_one_counts.txt"
os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
if os.path.exists(filename):
  df = pd.read_csv(filename)
  words = df["words"].values.tolist()
  counts = df["counts"].values.tolist()

words = words[:len(translations)]
counts = counts[:len(translations)]

df = create_df(words, counts, translations)

df.to_csv("translated_word_frequency.txt")
