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

def store_list_new(arr, file_name):
  # with open(file_name, "r") as f:
  #   content = f.read()
  #   f.close()

  f = open(file_name, "r")
  content = f.read()
  f.close()

  content = content.split("\n")
  for content_word in content:
    if not content_word.strip():
      content.remove(content_word)
  
  arr = content + arr

  with open(file_name, "w") as f:
    for line in arr:
      f.write(line + "\n")
    f.close()

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
    # print('_'*50)
    # print('Original    :', text)
    # print('Translation :', content)
    # print('_'*50)
  return output_list

def translate_text_new(list_to_translate, complete_list, save_file_name, index_to_store=100):
  PATH = "C:\Program Files (x86)\chromedriver.exe"
  driver = webdriver.Chrome(PATH)
  deepl_url = 'https://www.deepl.com/en/translator'
  driver.get(deepl_url)
  time.sleep(3)
  # cookie_button = driver.find_element_by_class_name("dl_cookieBanner--cta-buttonClose")
  cookie_button = driver.find_element_by_class_name("dl_cookieBanner--cta-buttons")
  cookie_button.find_element_by_tag_name("button").click()
  output_list = []
  i = 0
  for word in list_to_translate:
    try:
      i += 1
      # Get thie inupt_area 
      # input_css = 'div.lmt__inner_textarea_container textarea'
      # input_area = driver.find_element_by_css_selector(input_css)

      input_area = driver.find_element_by_class_name("lmt__inner_textarea_container")
      input_area = input_area.find_element_by_tag_name("textarea")

      # Send the text
      input_area.clear() 
      input_area.send_keys(word)

      # Wait for translation to appear on the web page
      time.sleep(3)

      buttons_to_translate = []

      # Get copybutton and click on it
      # button = driver.find_element_by_xpath('//*[@id="panelTranslateText"]/div[3]/section[2]/div[3]/div[6]/div/div[3]')
      try:
        cc_button = driver.find_element_by_xpath('//*[@id="panelTranslateText"]/div[3]/section[2]/div[3]/div[6]/div/div[3]')
      except Exception as e:
        print("")
      try:
        cc_button = driver.find_element_by_xpath('//*[@id="panelTranslateText"]/div[3]/section[2]/div[7]/div/div[3]')
      except Exception as e:
        print("")

      buttons_to_translate = driver.find_elements_by_class_name("lmt__translations_as_text__item")
        
      trans_for_one_word = str(word) + "|"
      # try:
      cc_button.click()
      # except Exception as e:
      #   error_fighting_for_translation(complete_list, save_file_name, index_to_store, output_list)
      time.sleep(0.2)
      # content = cc_button.text
      # Get content from clipboard
      content = clipboard.paste()
      # print(content)
      trans_for_one_word += content
      clipboard.copy('ERROR___ERROR')
      for button in buttons_to_translate:
          button = button.find_element_by_tag_name("button")
          text_to_add = button.text
          if text_to_add.strip() != "": 
          #   text_to_add.replace("\n", "")
            text_to_add = text_to_add.replace(" .", "")
            text_to_add = text_to_add.replace(".", "")
            text_to_add = text_to_add.replace(":", "")
            text_to_add = text_to_add.replace(",", "")
            trans_for_one_word += ("|" + text_to_add)

        # store_list(content, store_file_name)
        # clipboard.copy('ERROR___ERROR')
      print(trans_for_one_word)
      output_list.append(trans_for_one_word)

      if len(output_list) >= index_to_store:
        store_list_new(output_list, save_file_name)
        output_list = []
    except Exception as e:
      # if(len(output_list) > 0):
      #   store_list_new(output_list, save_file_name)
      # with open(save_file_name, "r") as f:
      #   content = f.read()
      #   content = content.split("\n")
      #   for content_word in content:
      #     if not content_word.strip():
      #       content.remove(content_word)
      #   last_translated_word = str(content[-1:]).split("|")[0]
      #   last_translated_word = last_translated_word.replace("'", "")
      #   last_translated_word = last_translated_word.replace("[", "")
      #   print(last_translated_word + "///")
      #   last_index = complete_list.index(last_translated_word)
      #   print("index of last word" + str(last_index))
      #   translate_text_new(complete_list[last_index + 1:], save_file_name, index_to_store)
      if(len(output_list) > 0):
        store_list_new(output_list, save_file_name)
      with open(save_file_name, "r") as f:
        content = f.read()
      content = content.split("\n")
      for content_word in content:
        if not content_word.strip():
          content.remove(content_word)
      last_translated_word = str(content[-1:]).split("|")[0]
      last_translated_word = last_translated_word.replace("'", "")
      last_translated_word = last_translated_word.replace("[", "")
      print(last_translated_word + "///")
      last_index = complete_list.index(last_translated_word)
      print("index of last word" + str(last_index))
      translate_text_new(complete_list[last_index + 1:], save_file_name, index_to_store)
      # error_fighting_for_translation(complete_list, save_file_name, index_to_store, output_list)
  return output_list

# def error_fighting_for_translation(complete_list, save_file_name, index_to_store, output_list):
#   if(len(output_list) > 0):
#       store_list_new(output_list, save_file_name)
#   time.sleep(0.2)
#   with open(save_file_name, "r") as f:
#     content = f.read()
#     f.close()
#   content = content.split("\n")
#   for content_word in content:
#     if not content_word.strip():
#       content.remove(content_word)
#   last_translated_word = str(content[-1:]).split("|")[0]
#   last_translated_word = last_translated_word.replace("'", "")
#   last_translated_word = last_translated_word.replace("[", "")
#   print(last_translated_word + "///")
#   last_index = complete_list.index(last_translated_word)
#   print("index of last word" + str(last_index))
#   translate_text_new(complete_list[last_index + 1:], save_file_name, index_to_store)

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
  filename = "new_word_list_edit.txt"
  os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
  if os.path.exists(filename):
    df = pd.read_csv(filename, encoding="utf-8")
    words = df["words"].values.tolist()
    # counts = df["counts"].values.tolist()
  else:
    print("error")

  # 81499 + 1
  # words = words[81500:]

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

filename = "new_word_list_edit.txt"
os.chdir("D:/Users/flopp/Documents/VSCode/Python/NLP")
if os.path.exists(filename):
  df = pd.read_csv(filename, encoding="utf-8")
  words = df["words"].values.tolist()

words_edit = words[1411:]
translate_text_new(words_edit, words, "new_word_list_trans.txt", 100)