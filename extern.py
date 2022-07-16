from posixpath import split
from venv import create
from selenium import webdriver
import time
import threading
import os
import pandas as pd
import re
import logging

def create_df(words, counts):
  df = pd.DataFrame(data={"counts": counts, "words": words})
  return df

def load_list(file_name):
  f = open(file_name, "r")
  content = f.read()
  f.close()

  words = []
  counts = []

  lines = content.split("\n")[1:]
  for line in lines:
    line = line.replace("  ", " ")
    line = line.replace("  ", " ")
    line = line.replace("  ", " ")
    line = line.replace("  ", " ")
    line = line.replace("  ", " ")
    line = line.replace("  ", " ")
    line = line.replace("  ", " ")

    line = line.split(" ")
    words.append(line[1].lower())
    counts.append(line[3][:-1].lower())

  return words, counts

def load_list_pd(file_name):
  df = pd.read_csv(file_name)
  words = df["words"]
  counts = df["counts"]
  return words, counts

def store_list_pd(df, file_name):
  df.to_csv(file_name)

def selenium(words_to_translate, batch_size, file_name):
  PATH = "C:\Program Files (x86)\chromedriver.exe"
  driver = webdriver.Chrome(PATH)
  url = "https://translate.google.com/?sl=en&tl=de&op=translate"
  driver.get(url)
  translations = []
  i = 0
  for word_to_translate in words_to_translate:
    i+=1
    if(i%batch_size == 0):
      try:
        f = open(file_name, "r")
        content = f.read()
        f.close()
      except:
        f = open(file_name, "w")
        content = ""
        f.close()
      for synonym_trans in translations:
        new_line = ""
        for single_trans in synonym_trans:
          single_trans = re.sub('[^a-zA-Z0-9\u00E4\u00F6\u00FC\u00C4\u00D6\u00DC\u00df\n]', '', single_trans)
          new_line += single_trans + ","
        content += new_line + "\n"
      f = open(file_name, "w")
      f.write(content)
      f.close()
      translations = []
    translations.append(get_trans_with_synonyms(driver, word_to_translate))

def get_trans_with_synonyms(driver, word):
  translations = []
  input_area = driver.find_element_by_class_name("er8xn")
  input_area.clear()
  try:
    input_area.send_keys(word)
    time.sleep(2)
    try:
      translation_text = driver.find_element_by_class_name("Q4iAWc").text
      translations.append(translation_text.strip())
    except:
      elements = driver.find_elements_by_class_name("VIiyi")
      for element in elements:
        translations.append(element.text.strip())
    try:
      synonym_translations = driver.find_elements_by_class_name("kgnlhe")
      for synonym in synonym_translations:
        try:
          if(synonym.text.strip() != ""):
            translations.append(synonym.text.strip())
        except:
          print("error with synonym adding")
    except:
      print("error with synonym getting")
  except:
    translations.append("$$_ERROR_$$")
  return translations

def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
  
# selenium("drive")
words, counts = load_list_pd("word_list_extern_pd.txt")
df = create_df(words, counts)
words = words[85678:95678]
# selenium(words, 100, "translations_multi_0.txt")

chunks = []

chunk_size = 2000

for i in list(chunk_list(words, chunk_size)):
  chunks.append(list(i))

num_chunks = len(chunks)

if __name__ == "__main__":
  format = "%(asctime)s: %(message)s"

  logging.basicConfig(format=format, level=logging.INFO,
                      datefmt="%H:%M:%S")


  logging.info("Main    : before creating thread")

  threads = []
  for i in range(num_chunks):
    threads.append(threading.Thread(target=selenium, args=(chunks[i], 100, f"translation_multi_{i}.txt")))

  logging.info("Main    : before running thread")


  for i in range(len(threads)):
    threads[i].start()
  logging.info("Main    : wait for the thread to finish")

  for i in range(len(threads)):
      threads[i].join()
  # x.join()

  logging.info("Main    : all done")
