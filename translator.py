from selenium import webdriver
import time
import clipboard
import os
import pandas as pd
import word_counter

def store_list(arr, file_name):
  os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
  try:
    df = pd.read_csv(file_name)
    loaded_output_list = df["translations"].values.tolist()
    arr = arr.splitlines()
    # arr = arr[:-1]
    arr = loaded_output_list + arr
    if "Übersetzt mit www.DeepL.com/Translator (kostenlose Version)" in arr:
      arr.remove("Übersetzt mit www.DeepL.com/Translator (kostenlose Version)")
    # for word in arr:
    #   word = str(word).replace('"', "")
    #   if not word.strip() or not word:
    #     arr.remove(word)
  
    df = pd.DataFrame(data={"translations": arr})
    df.to_csv(file_name)
  except Exception as e:
    arr = arr.splitlines()
    arr = arr[:-3]
    df = pd.DataFrame(data={"translations": arr})
    df.to_csv(file_name)
  


def translate_text(text_list, store_file_name):
  PATH = "C:\Program Files (x86)\chromedriver.exe"
  driver = webdriver.Chrome(PATH)
  deepl_url = 'https://www.deepl.com/en/translator'
  driver.get(deepl_url)
  cookie_button = driver.find_element_by_class_name("dl_cookieBanner--cta-buttons")
  cookie_button.find_element_by_tag_name("button").click()
  time.sleep(3)
  output_list = []
  i = 0
  for text in text_list:
    i += 1

    # Get thie inupt_area 
    input_css = 'div.lmt__inner_textarea_container textarea'
    input_area = driver.find_element_by_css_selector(input_css)

    # Send the text
    input_area.clear() 
    input_area.send_keys(text)

    # Wait for translation to appear on the web page
    time.sleep(11)

    # Get copybutton and click on it
    # button = driver.find_element_by_xpath('//*[@id="panelTranslateText"]/div[3]/section[2]/div[3]/div[6]/div/div[3]')
    try:
      button = driver.find_element_by_xpath('//*[@id="panelTranslateText"]/div[3]/section[2]/div[3]/div[6]/div/div[3]')
    except Exception as e:
      print(e)
    try:
      button = driver.find_element_by_xpath('//*[@id="panelTranslateText"]/div[3]/section[2]/div[7]/div/div[3]')
    except Exception as e:
      print(e) 

    
    button.find_element_by_tag_name("button").click()
    # button = driver.find_element_by_class_name("button--2IZ9p")
    button.click()

    # Get content from clipboard
    content = clipboard.paste()
    # output_list.append(content)
    store_list(content, store_file_name)
    clipboard.copy('')

    # Quit selenium driver
    # driver.quit()

    # Display results
    print('_'*50)
    # print('Original    :', text)
    # print('Translation :', content)
    print('_'*50)
  return output_list

def refurbish_translations(load_file_name, store_file_name):
  if os.path.exists(load_file_name):
    df = pd.read_csv(load_file_name)
    loaded_output_list = df["translations"].values.tolist()

  single_word_list = []
  for translation in loaded_output_list:
    single_words = translation.split("\n")
    for word in single_words:
      # word = word.replace("\n", "")	
      word = word.replace('"', '')
      word = word.replace("  ", " ")
      word = word.replace("Übersetzt mit www.DeepL.com/Translator (kostenlose Version)", "")
      if word.strip():
        single_word_list.append(word)

    with open(store_file_name, 'w', encoding="utf-8") as f:
      for word in single_word_list:
        f.write("%s" % word)

def create_df(words, counts, translations):
  df = pd.DataFrame(data={"counts": counts, "words": words, "translations": translations})
  return df

def create_batch_list(list, batch_size):
  batch_list = []

  for i in range(0, len(list), batch_size):
    batch_list.append(list[i:i+batch_size])
  
  for i in range(len(batch_list)):
    for a in range(len(batch_list[i])):
      batch_list[i][a] = str(batch_list[i][a]) + "\n"

  return batch_list

def translate():
  filename = "word_frequency_no_one_counts.txt"
  os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
  if os.path.exists(filename):
    df = pd.read_csv(filename, encoding="utf-8")
    words = df["words"].values.tolist()
    # counts = df["counts"].values.tolist()
  else:
    print("error")

  # 81499 + 1
  words = words[81500:]

  batches = create_batch_list(words, 500)

  translate_text(batches, "translations.txt")

def filter_df():

  os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
  df = pd.read_csv("complete.txt")

  translations = df["translations"].values.tolist()
  words = df["words"].values.tolist()
  counts = df["counts"].values.tolist()

  new_translations = []
  new_words = []
  new_counts = []

  for i in range(len(words)):
    translation = str(translations[i]).lower()
    word = str(words[i]).lower()
    if translation != word:
      new_translations.append(translation)
      new_words.append(word)
      new_counts.append(counts[i])

  df = create_df(new_words, new_counts, new_translations)
  df.to_csv("complete_new.txt", encoding="utf-8")

counter = word_counter.NumCounter()
counter.normalize_counts("complete_new.txt", "complete_new.txt")